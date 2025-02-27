from sqlalchemy.orm import Session
from app.models import Location
from app.schemas import LocationSchema

def save_location(db: Session, location: LocationSchema):
    new_location = Location(**location.model_dump())  # Fix for Pydantic v2
    db.add(new_location)
    db.commit()
    db.refresh(new_location)  # Ensures latest DB state is returned
    return new_location
