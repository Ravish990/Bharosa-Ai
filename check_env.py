import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Print values to check if they're loaded correctly
print("TWILIO_ACCOUNT_SID:", os.getenv("TWILIO_ACCOUNT_SID"))
print("TWILIO_AUTH_TOKEN:", os.getenv("TWILIO_AUTH_TOKEN"))
print("TWILIO_WHATSAPP_NUMBER:", os.getenv("TWILIO_WHATSAPP_NUMBER"))
