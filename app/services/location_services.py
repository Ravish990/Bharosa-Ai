from sqlalchemy.orm import Session
from app.models import Location
from app.schemas import LocationSchema

def save_location(db: Session, location: LocationSchema):
    new_location = Location(**location.dict())
    db.add(new_location)
    db.commit()
    return new_location
