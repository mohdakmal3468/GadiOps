from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.vehicle import Vehicle
from app.models.expense import MaintenanceLog

class MaintenanceService:
    @staticmethod
    def create_maintenance(db: Session, vehicle_id: int, description: str, cost: float, log_date: date):
        # 1. Check vehicle
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # 2. Create log and force status to "In Shop"
        log = MaintenanceLog(vehicle_id=vehicle_id, description=description, cost=cost, date=log_date, is_active=1)
        vehicle.status = "In Shop"
        
        db.add(log)
        db.commit()
        return log

    @staticmethod
    def close_maintenance(db: Session, log_id: int):
        log = db.query(MaintenanceLog).filter(MaintenanceLog.id == log_id).first()
        if not log or not log.is_active:
            raise HTTPException(status_code=400, detail="Maintenance already closed or not found")
        
        # 3. Restore vehicle to "Available"
        vehicle = db.query(Vehicle).filter(Vehicle.id == log.vehicle_id).first()
        log.is_active = 0
        vehicle.status = "Available"
        
        db.commit()
        return {"detail": "Maintenance closed and vehicle restored to Available"}