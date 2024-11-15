# # email_sender.py
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import openai
# from config import OPENAI_API_KEY, FROM_EMAIL, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT

# openai.api_key = OPENAI_API_KEY

# def generate_email_content(row, prompt_template):
#     try:
#         prompt = prompt_template.format(**row)
#         response = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=prompt,
#             max_tokens=100
#         )
#         return response.choices[0].text
#     except Exception as e:
#         print(f"Error generating email content: {e}")
#         return None

# def send_bulk_emails(email_data, prompt_template):
#     results = []
#     try:
#         # Set up the SMTP connection
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls()  # Start TLS encryption
#         server.login(FROM_EMAIL, EMAIL_PASSWORD)

#         for row in email_data:
#             content = generate_email_content(row, prompt_template)
#             if content is None:
#                 results.append({"email": row.get("email"), "status": "Failed", "error": "Content generation failed"})
#                 continue

#             # Create the email
#             msg = MIMEMultipart()
#             msg['From'] = FROM_EMAIL
#             msg['To'] = row['email']
#             msg['Subject'] = "Your Custom Email"
#             msg.attach(MIMEText(content, 'html'))

#             # Send the email
#             server.sendmail(FROM_EMAIL, row['email'], msg.as_string())
#             results.append({"email": row.get("email"), "status": "Sent"})

#         server.quit()
#     except Exception as e:
#         print(f"Error sending emails: {e}")
#         results.append({"error": str(e)})

#     return {"results": results}

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
from config import SMTP_SERVER, SMTP_PORT, FROM_EMAIL, EMAIL_PASSWORD, OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_email_content(row, prompt_template):
    try:
        prompt = prompt_template.format(**row)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text
    except Exception as e:
        print(f"Error generating email content: {e}")
        return None

def send_email(recipient, subject, content):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(FROM_EMAIL, EMAIL_PASSWORD)

        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(content, 'html'))

        server.sendmail(FROM_EMAIL, recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_bulk_emails(email_data, prompt_template):
    results = []
    for row in email_data:
        content = generate_email_content(row, prompt_template)
        if content:
            success = send_email(row['email'], "Custom Email", content)
            results.append({"email": row['email'], "status": "Sent" if success else "Failed"})
        else:
            results.append({"email": row['email'], "status": "Failed", "error": "Content generation failed"})
    return results
