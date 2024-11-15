## Custom Email Sender Application

This is a Flask application that allows users to upload CSV data, customize email prompts, and send personalized emails. It uses OpenAI for content generation and SendGrid for email delivery.

## Setup Instructions

1. Clone the repository and navigate to the project folder.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt

## Run the Application

1. Start the Celery worker:
   ```bash
   celery -A scheduler worker --loglevel=info
2. Run the Flask app:
   ```bash
   python app.py
3. Open the app in your browser:
   ```bash
   http://127.0.0.1:5000
