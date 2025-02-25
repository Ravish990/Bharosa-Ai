from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Location
from app.schemas import LocationSchema

router = APIRouter(prefix="/api/location", tags=["Location"])

@router.post("/share")
def share_location(location: LocationSchema, db: Session = Depends(get_db)):
    new_location = Location(**location.dict())
    db.add(new_location)
    db.commit()
    return {"message": "Location shared successfully!"}

@router.get("/{user_id}")
def get_location(user_id: str, db: Session = Depends(get_db)):
    location = db.query(Location).filter(Location.user_id == user_id).order_by(Location.id.desc()).first()
    if not location:
        raise HTTPException(status_code=404, detail="No location found")
    return {"latitude": location.latitude, "longitude": location.longitude, "timestamp": location.timestamp}
