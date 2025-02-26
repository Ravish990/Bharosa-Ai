import os
from fastapi import APIRouter, UploadFile, File
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Temporary storage for trusted contacts (Replace with a database later)
trusted_contacts = {}  # user_id -> list of trusted phone numbers

# API to receive recorded voice and notify trusted contacts via WhatsApp
@router.post("/api/voice_alert")
async def voice_alert(user_id: str, audio: UploadFile = File(...)):
    audio_path = f"app/uploads/{user_id}_alert.wav"

    # Save the uploaded audio file
    with open(audio_path, "wb") as buffer:
        buffer.write(await audio.read())

    # Generate a temporary download link for the voice message
    voice_link = f"http://yourserver.com/uploads/{user_id}_alert.wav"

    # Send the voice alert via WhatsApp
    if user_id in trusted_contacts:
        for phone_number in trusted_contacts[user_id]:
            send_whatsapp_alert(phone_number, voice_link)

    return {"message": "Voice alert sent successfully"}

# Function to send a WhatsApp message
def send_whatsapp_alert(phone_number, voice_link):
    whatsapp_url = f"https://wa.me/{phone_number}?text=" + \
                   f"Emergency Alert! 🚨 A voice message has been recorded. Listen here: {voice_link}"
    print(f"WhatsApp message ready to send: {whatsapp_url}")
