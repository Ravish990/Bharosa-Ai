from pydantic import BaseModel

class LocationSchema(BaseModel):
    user_id: str
    latitude: float
    longitude: float
    timestamp: int
