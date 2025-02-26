from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(Integer)

class TrustedContact(Base):
    __tablename__ = "trusted_contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("locations.user_id"), index=True)
    phone_number = Column(String, index=True)  # Store phone numbers instead of emails

    user = relationship("Location", back_populates="contacts")

# Add this relationship in the Location model
Location.contacts = relationship("TrustedContact", back_populates="user")
