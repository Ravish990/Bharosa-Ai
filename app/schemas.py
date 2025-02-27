from pydantic import BaseModel

class LocationSchema(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    timestamp: int

    class Config:
        from_attributes = True  # Allows ORM model conversion
