import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Blueprint, jsonify, request, current_app
import os

research_bp = Blueprint('company_name', __name__)

@research_bp.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    subject = data.get('subject')
    body = data.get('body')
    recipient = data.get('recipient')

    # Retrieve sender email and password from environment variables
    sender_email = os.environ.get("UEMAIL")
    sender_password = os.environ.get("PASSWORDS")

    if not sender_email or not sender_password:
        return jsonify({"error": "Sender email or password not set in environment variables"}), 400

    try:
        # Set up the SMTP server and login
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()  # Encrypts the connection
        smtp_server.login(sender_email, sender_password)

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        # Attach the body with the msg
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        smtp_server.sendmail(sender_email, recipient, msg.as_string())
        smtp_server.quit()  # Close the connection

        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
