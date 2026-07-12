from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String, unique=True, index=True, nullable=False) # Mandated unique index
    model = Column(String, nullable=False)
    vehicle_type = Column(String, nullable=False) # e.g., Van, Truck, Sedan[cite: 1]
    max_load_capacity = Column(Float, nullable=False) # in kg[cite: 1]
    odometer = Column(Float, default=0.0, nullable=False)
    acquisition_cost = Column(Float, nullable=False)
    
    # Tracked state metrics: Available, On Trip, In Shop, Retired[cite: 1]
    status = Column(String, default="Available", nullable=False)