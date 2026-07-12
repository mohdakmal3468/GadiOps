from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from app.core.database import Base

# --- Existing MaintenanceLog from previous step is here ---

class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True) # Optional link to a specific trip
    liters = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    date = Column(Date, nullable=False)


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    category = Column(String, nullable=False) # e.g., Tolls, Permits, Insurance, Fines
    cost = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=True)

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    description = Column(String, nullable=False)
    cost = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    is_active = Column(Integer, default=1) # 1 = Active (In Shop), 0 = Closed (Available)