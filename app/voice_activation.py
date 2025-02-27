import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from dotenv import load_dotenv
from twilio_service import send_whatsapp_message  # ✅ Correct
# Import Twilio function from twilio_service.py

# Load environment variables
load_dotenv()

router = APIRouter()

# API to receive recorded voice and notify trusted contacts via WhatsApp
@router.post("/api/voice_alert")
async def voice_alert(user_id: str, audio: UploadFile = File(...)):
    from app.main import trusted_contacts  # ✅ Moved import inside the function

    upload_dir = "app/uploads"
    os.makedirs(upload_dir, exist_ok=True)  # Ensure uploads directory exists

    audio_path = os.path.join(upload_dir, f"{user_id}_alert.wav")

    # Save the uploaded audio file
    with open(audio_path, "wb") as buffer:
        buffer.write(await audio.read())

    # Generate a temporary link (Modify this based on your server settings)
    server_url = os.getenv("SERVER_URL", "http://localhost:8000")  # Use an env variable for flexibility
    voice_link = f"{server_url}/uploads/{user_id}_alert.wav"

    # Check if the user has trusted contacts
    if user_id not in trusted_contacts or not trusted_contacts[user_id]:
        raise HTTPException(status_code=400, detail="No trusted contacts found for this user.")

    # Send the WhatsApp alert
    for phone_number in trusted_contacts[user_id]:
        message = f"🚨 Emergency Alert!\nA voice message has been recorded. Listen here: {voice_link}"
        send_whatsapp_message(phone_number, message)

    return {"message": "Voice alert sent successfully", "voice_link": voice_link}
