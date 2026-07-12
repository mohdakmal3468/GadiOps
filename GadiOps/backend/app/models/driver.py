from sqlalchemy import Column, Integer, String, Date, Float
from app.core.database import Base

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license_number = Column(String, unique=True, index=True, nullable=False)
    license_category = Column(String, nullable=False) # e.g., Class A, Heavy Truck
    license_expiry_date = Column(Date, nullable=False) # Mandated tracking field[cite: 1]
    contact_number = Column(String, nullable=False)
    safety_score = Column(Float, default=100.0, nullable=False) # Scale 0 - 100[cite: 1]
    
    # Tracked state metrics: Available, On Trip, Off Duty, Suspended[cite: 1]
    status = Column(String, default="Available", nullable=False)