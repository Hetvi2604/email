from celery import Celery
from email_sender import send_bulk_emails

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def schedule_emails(email_data, prompt_template):
    return send_bulk_emails(email_data, prompt_template)
