import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables
load_dotenv()

# Get Twilio credentials from .env
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Function to send WhatsApp message
def send_whatsapp_message(to_number, message):
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("❌ ERROR: Twilio credentials are missing.")
        return {"status": "error", "error": "Twilio credentials are missing"}

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=f"whatsapp:{to_number}"
        )
        print(f"✅ Message sent successfully! SID: {msg.sid}")
        return {"status": "success", "message_sid": msg.sid}

    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        return {"status": "error", "error": str(e)}
