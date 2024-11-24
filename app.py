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

# Flask app initialization
app = Flask(__name__)

# Email credentials
sender_email = "Youremail"
sender_password = "Password"

# API key configuration (ensure your key is valid)
genai.configure(api_key="apikey")

# Prompt for generating content in CSV format
messagetoCsvPrompt = '''Use the below information and return the output in this csv format:
CompanyName,Role,Experience,Location,Applicationlink,Email
If some values are not available, use "nan".
'''

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "response_mime_type": "text/plain",
}

# Create the model instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def send_email(sender_email, sender_password, recipient_email, subject, body, attachment_path):
    """Send an email with attachment."""
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

def messageToCsv(data, csv_filename='data.csv'):
    """Writes the provided data to a CSV file."""
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def generateJobData(input_data):
    """Generates job data from input using the generative model."""
    try:
        response = model.generate_content([messagetoCsvPrompt] + input_data.split("\n"))
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

        job_data = generateJobData(input_details)

        if job_data:
            messageToCsv(job_data, 'output_jobs.csv')
            # Read the CSV file and send emails
            with open('output_jobs.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 6:  # Ensure the row has at least 6 columns
                        name, role, experience, location, applicationlink, email = row

                        if name != "nan":
                            subject = model.generate_content(f'use the below data to apply for the {role} for {name} for following job write a subject only give a normal '+userData()).text
                            body = model.generate_content(f'use the below data to apply for the {role} for {name} for experience year of {experience} at {location} for following job write a mail only give a normal body for mail do not use any place holders all details are mentionedn and over exacurate my profile '+userData()).text
                            attachment_path = 'resume_Research.pdf'

                            send_email(sender_email, sender_password, email, subject, body, attachment_path)
            return "Emails sent successfully!"

        return "No data to process.", 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
