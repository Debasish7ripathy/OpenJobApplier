from flask import Flask, request, render_template, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import google.generativeai as genai
import csv
from pdf import userData

app = Flask(__name__)


SENDER_EMAIL = "debasish.tripathy.Sinecures@gmail.com"
SENDER_PASSWORD = "xied dyck igbd egjz"

genai.configure(api_key="AIzaSyC9D-mcei5-pvXF0lZnzYGLm7BFSlSyLpM")

CSV_PROMPT = '''Use the below information and return the output in this CSV format:
CompanyName, Role, Experience, Location, ApplicationLink, Email
If any values are not available, use "nan".
'''

GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=GENERATION_CONFIG,
)

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        filename = os.path.basename(attachment_path)
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(part)
    except Exception as e:
        print(f"Error attaching file: {e}")
        return

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            print(f"Email sent to {recipient_email} successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def message_to_csv(data, csv_filename='data.csv'):
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def generate_job_data(input_data):
    try:
        response = model.generate_content([CSV_PROMPT] + input_data.split("\n"))
        response_text = response.text.replace("```csv", "").replace("```", "")
        print(f"Generated response:\n{response_text}")

        rows = []
        for line in response_text.splitlines():
            row = [value.strip() if value.strip() else "nan" for value in line.split(",")]
            rows.append(row)

        return rows
    except Exception as e:
        print(f"Error during generation: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_details = request.form.get('job_description', '').strip()
        if not input_details:
            return "No job description provided.", 400

        job_data = generate_job_data(input_details)

        if job_data:
            message_to_csv(job_data, 'output_jobs.csv')

            with open('output_jobs.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 6:
                        company_name, role, experience, location, application_link, email = row

                        if company_name != "nan":
                            subject_prompt = f"Generate a subject line for a job application for {role} at {company_name}."
                            subject = model.generate_content(f'use the below data to apply for the {role} for {company_name} for following job write a subject only give a normal '+userData()).text

                            body_prompt = (
                                f"Write a professional email for {company_name} applying for the {role} position at {location}. "
                                f"{company_name} has {experience} years of experience in the industry and is highly skilled in relevant areas. "
                                "Provide a formal yet convincing body for the email, highlighting the candidate's expertise "
                                "and enthusiasm for the role, without using any placeholders or over-exaggerating the profile. "
                                "Ensure the content is well-structured, concise, and clear."
                                f"and use {userData()} to attach the resume."
                                "make sure not to use any placeholders "
                            )
                            body = model.generate_content(body_prompt).text

                            attachment_path = 'Resume_Debasish_Research.pdf'

                            send_email(SENDER_EMAIL, SENDER_PASSWORD, email, subject, body, attachment_path)

            return "Emails sent successfully!"

        return "No data to process.", 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
