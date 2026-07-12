from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.maintenance_service import MaintenanceService
from app.routers.auth import get_current_user

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.models.expense import FuelLog, Expense, MaintenanceLog
from app.models.vehicle import Vehicle
from app.schemas.expense import FuelLogCreate, FuelLogResponse, ExpenseCreate, ExpenseResponse
from app.models.user import User

router = APIRouter(prefix="/expenses", tags=["Fuel & Expense Management"])

# ==========================================
# 1. LOG FUEL LOG
# ==========================================
@router.post("/fuel", response_model=FuelLogResponse, status_code=status.HTTP_201_CREATED)
def log_fuel(payload: FuelLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Logs fuel data for a vehicle."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    new_fuel_log = FuelLog(**payload.model_dump())
    db.add(new_fuel_log)
    db.commit()
    db.refresh(new_fuel_log)
    return new_fuel_log

# ==========================================
# 2. LOG MISCELLANEOUS EXPENSE
# ==========================================
@router.post("/misc", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def log_misc_expense(payload: ExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Logs an operational expense like tolls or permits."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
        
    new_expense = Expense(**payload.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

# ==========================================
# 3. GET TOTAL OPERATIONAL COST PER VEHICLE
# ==========================================
@router.get("/operational-cost/{vehicle_id}")
def get_vehicle_operational_cost(vehicle_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Automatically computes total operational cost (Fuel + Maintenance + Misc) per vehicle[cite: 1].
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Aggregate Fuel Costs
    total_fuel = db.query(func.sum(FuelLog.cost)).filter(FuelLog.vehicle_id == vehicle_id).scalar() or 0.0
    
    # Aggregate Maintenance Costs
    total_maint = db.query(func.sum(MaintenanceLog.cost)).filter(MaintenanceLog.vehicle_id == vehicle_id).scalar() or 0.0
    
    # Aggregate Misc Costs
    total_misc = db.query(func.sum(Expense.cost)).filter(Expense.vehicle_id == vehicle_id).scalar() or 0.0

    return {
        "vehicle_id": vehicle_id,
        "registration_number": vehicle.registration_number,
        "fuel_cost": total_fuel,
        "maintenance_cost": total_maint,
        "miscellaneous_cost": total_misc,
        "total_operational_cost": total_fuel + total_maint + total_misc[cite: 1]
    }

@router.post("")
def add_maintenance(vehicle_id: int, desc: str, cost: float, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return MaintenanceService.create_maintenance(db, vehicle_id, desc, cost, date.today())

@router.post("/{log_id}/close")
def close_maintenance(log_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return MaintenanceService.close_maintenance(db, log_id)