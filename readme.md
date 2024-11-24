
# Job Data Generator and Email Sender

This project is a web application that allows users to input job descriptions, generate job data using an AI model, and send application emails automatically. It's built using Flask, a web framework for Python.

## Features

- Input job descriptions through a web form.
- Generate structured job data using a generative AI model.
- Automatically send application emails with an attached resume.

## Requirements

Before you begin, ensure you have met the following requirements:

- **Python**: Make sure Python 3.x is installed on your system. You can download it from [python.org](https://www.python.org/).
- **Flask**: This web application requires Flask. You can install it using pip (Python's package manager).

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**: If you have Git installed, run the following command to clone the repository. If not, you can download the ZIP file from the repository.

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Required Packages**: Open a terminal or command prompt in the project directory and run the following command to install Flask and other dependencies:

   ```bash
   pip install Flask
   ```

3. **Install Additional Libraries**: Ensure you have access to the required libraries for email sending and AI generation:

   ```bash
   pip install google-generativeai
   ```

4. **Set Up Environment Variables**: For security reasons, do not hardcode sensitive information such as email credentials. Instead, set them as environment variables on your operating system. Here's how:

   - **On Windows**:
     1. Open Command Prompt.
     2. Run `set FLASK_APP=app.py`
     3. Run `set FLASK_ENV=development`
     4. Run `set EMAIL_USER=your_email@gmail.com`
     5. Run `set EMAIL_PASS=your_email_password`

   - **On macOS/Linux**:
     1. Open Terminal.
     2. Run `export FLASK_APP=app.py`
     3. Run `export FLASK_ENV=development`
     4. Run `export EMAIL_USER=your_email@gmail.com`
     5. Run `export EMAIL_PASS=your_email_password`

## Usage

To start the application, follow these steps:

1. **Run the Flask Application**: In your terminal or command prompt, ensure you are in the project directory, then run:

   ```bash
   flask run
   ```

2. **Access the Web Application**: Open your web browser and go to `http://127.0.0.1:5000/`. You will see a form where you can input job descriptions.

3. **Input Job Descriptions**: Enter each job description on a new line in the provided text area and click "Generate and Send Emails."

4. **Email Sending**: The application will process the job descriptions, generate the necessary data, and send application emails to the specified addresses.

## Configuration

- **Resume Attachment**: Ensure your resume file is named `Resume_Debasish_Research.pdf` and is located in the project directory. Update the file path in the code if your resume is named differently or located elsewhere.

- **AI Model Configuration**: The application uses a generative AI model to process input data. Ensure you have a valid API key for the `google-generativeai` library and that it is correctly configured in the application code.

## Troubleshooting

- **Common Issues**: If you encounter any issues, check the terminal for error messages. Ensure all required packages are installed and that all environment variables are correctly set.

- **Security**: Never share your email password or API key publicly. Use environment variables to keep them secure.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please create a pull request or submit an issue.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the developers of Flask and other open-source libraries used in this project.
- Special thanks to [Your Name] for developing and maintaining this project.

