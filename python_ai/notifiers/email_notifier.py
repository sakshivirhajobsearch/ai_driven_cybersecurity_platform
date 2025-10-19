# email_notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ----------------- CONFIG -----------------
SMTP_HOST = "smtp.yourmail.com"
SMTP_PORT = 587  # 465 for SSL, 587 for TLS
SMTP_USER = "your_email@domain.com"
SMTP_PASSWORD = "your_email_password"
FROM_EMAIL = "your_email@domain.com"
# ------------------------------------------

def send_email(subject, message, to_email):
    """
    Send Email via SMTP
    :param subject: string, email subject
    :param message: string, email body
    :param to_email: string, recipient email
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls()  # Enable TLS
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
