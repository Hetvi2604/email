from flask import Flask, request, render_template, jsonify
import pandas as pd
from scheduler import schedule_emails
from email_sender import send_bulk_emails

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html') 

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    data = pd.read_csv(file)
    return jsonify({"status": "success", "data": data.to_dict(orient="records")})

@app.route('/send_emails', methods=['POST'])
def send_emails_route():
    data = request.json
    email_data = data.get('email_data')
    prompt = data.get('prompt')
    results = send_bulk_emails(email_data, prompt)
    return jsonify(results)

@app.route('/schedule_emails', methods=['POST'])
def schedule_emails_route():
    data = request.json
    email_data = data.get('email_data')
    prompt = data.get('prompt')
    task = schedule_emails.delay(email_data, prompt)
    return jsonify({"task_id": task.id, "status": "Scheduled"})

if __name__ == '__main__':
    app.run(debug=True)
