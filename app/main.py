import os
import time
import urllib.parse
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List
from dotenv import load_dotenv
from app.voice_activation import router as voice_router
from app.database import SessionLocal
from app.models import Location

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Mount the "uploads" directory to serve voice alerts
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# Include voice activation router
app.include_router(voice_router)

# Temporary in-memory storage (Replace with a database later)
trusted_contacts: Dict[str, List[str]] = {}  # user_id -> list of trusted contacts

class LocationData(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    timestamp: int
    trusted_contacts: List[str]  # Phone numbers of trusted contacts

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Store trusted contacts at login
@app.post("/api/trusted_contacts")
async def store_trusted_contacts(data: dict):
    try:
        user_id = data.get("user_id")
        contacts = data.get("trusted_contacts", [])

        if not user_id or not isinstance(contacts, list):
            raise HTTPException(status_code=400, detail="Invalid data format")

        trusted_contacts[user_id] = contacts
        return {"message": "Trusted contacts saved successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# API to share location (Now storing in database)
@app.post("/api/location/share")
async def share_location(location: LocationData, db=Depends(get_db)):
    try:
        # Save location in database
        new_location = Location(
            user_id=location.user_id,
            latitude=location.latitude,
            longitude=location.longitude,
            timestamp=location.timestamp or int(time.time())  # Use current timestamp if missing
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)

        # Generate WhatsApp shareable link (Encoded properly)
        message = f"🚨 Emergency! Please check my live location: https://www.google.com/maps?q={location.latitude},{location.longitude}"
        encoded_message = urllib.parse.quote(message)  # Encode spaces, special characters

        whatsapp_links = [
            f"https://wa.me/{contact}?text={encoded_message}" for contact in location.trusted_contacts
        ]

        return {"message": "Location shared successfully", "whatsapp_links": whatsapp_links}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
