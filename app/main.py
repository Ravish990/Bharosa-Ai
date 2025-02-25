import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Temporary in-memory storage (Replace with a database later)
user_locations: Dict[str, dict] = {}  
trusted_contacts: Dict[str, List[str]] = {}  # user_id -> list of trusted contacts

class LocationData(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    timestamp: int
    trusted_contacts: List[str]  # Emails of trusted contacts

# Store trusted contacts at login
@app.post("/api/trusted_contacts")
async def store_trusted_contacts(data: dict):
    user_id = data["user_id"]
    contacts = data["trusted_contacts"]
    trusted_contacts[user_id] = contacts
    return {"message": "Trusted contacts saved successfully"}

# API to share location
@app.post("/api/location/share")
async def share_location(location: LocationData):
    user_locations[location.user_id] = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "timestamp": location.timestamp,
    }

    # Send notifications to trusted contacts via email
    if location.user_id in trusted_contacts:
        for contact_email in trusted_contacts[location.user_id]:
            print(f"📩 Sending email to: {contact_email}")
            send_email_notification(contact_email, location.user_id, location.latitude, location.longitude)

    return {"message": "Location shared successfully"}

# Function to send email notifications
def send_email_notification(recipient_email, sender_id, lat, lon):
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("❌ ERROR: Email credentials are missing!")
        return

    msg = EmailMessage()
    msg["Subject"] = "Live Location Shared"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = recipient_email
    msg.set_content(f"{sender_id} has shared their location: https://www.google.com/maps?q={lat},{lon}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {recipient_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
