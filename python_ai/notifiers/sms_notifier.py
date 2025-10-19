# sms_notifier.py
from twilio.rest import Client

# ----------------- CONFIG -----------------
TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio phone number
# ------------------------------------------

def send_sms(message, to_number):
    """
    Send SMS using Twilio
    :param message: string, message to send
    :param to_number: string, recipient phone number with country code
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"SMS sent successfully to {to_number}, SID: {msg.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")
