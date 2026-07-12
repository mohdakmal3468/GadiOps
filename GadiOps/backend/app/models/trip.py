from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

# Open backend/app/models/trip.py and verify/append this field:
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Trip(Base):
    __tablename__ = "trips"

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    cargo_weight = Column(Float, nullable=False)
    planned_distance = Column(Float, nullable=False)
    status = Column(String, default="Draft", nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    
    # New parameter required to calculate absolute ROI
    revenue = Column(Float, default=0.0, nullable=False)

class Trip(Base):
    __tablename__ = "trips"

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    cargo_weight = Column(Float, nullable=False) # in kg
    planned_distance = Column(Float, nullable=False) # in km
    
    # State values: Draft, Dispatched, Completed, Cancelled[cite: 1]
    status = Column(String, default="Draft", nullable=False)
    
    # Database relationships linking external resources
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)