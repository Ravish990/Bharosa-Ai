import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from dotenv import load_dotenv
from app.voice_activation import router as voice_router

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
app.include_router(voice_router)

# Temporary in-memory storage (Replace with a database later)
user_locations: Dict[str, dict] = {}
trusted_contacts: Dict[str, List[str]] = {}  # user_id -> list of trusted contacts

class LocationData(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    timestamp: int
    trusted_contacts: List[str]  # Phone numbers of trusted contacts

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

    # Generate WhatsApp shareable link
    whatsapp_message = f"Emergency! Please check my live location: https://www.google.com/maps?q={location.latitude},{location.longitude}"
    
    whatsapp_links = [
        f"https://wa.me/{contact}?text={whatsapp_message}" for contact in location.trusted_contacts
    ]
    
    return {"message": "Location shared successfully", "whatsapp_links": whatsapp_links}
