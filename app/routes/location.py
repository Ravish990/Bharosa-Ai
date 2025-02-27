from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Location
from app.database import SessionLocal
from app.twilio_service import send_whatsapp_message
import time

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/location/share")
async def share_location(user_id: str, latitude: float, longitude: float, trusted_contacts: list, db: Session = Depends(get_db)):
    try:
        # Save location in database
        location = Location(user_id=user_id, latitude=latitude, longitude=longitude, timestamp=int(time.time()))
        db.add(location)
        db.commit()
        db.refresh(location)

        # Create message content
        message = f"🚨 Emergency Alert!\nUser {user_id} has shared their live location.\n📍 Latitude: {latitude}\n📍 Longitude: {longitude}\n\nStay safe! - BharosaAI"

        # Send WhatsApp message to all trusted contacts
        failed_contacts = []
        for contact in trusted_contacts:
            success = send_whatsapp_message(contact, message)
            if not success:
                failed_contacts.append(contact)

        # Handle failed messages
        if failed_contacts:
            return {
                "message": "Location shared but failed to send WhatsApp to some contacts.",
                "failed_contacts": failed_contacts
            }

        return {"message": "Location shared and WhatsApp alert sent!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
