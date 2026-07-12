from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.models.user import User

router = APIRouter(prefix="/vehicles", tags=["Vehicle Registry"])

# ==========================================
# 1. CREATE VEHICLE
# ==========================================
@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Secure endpoint verification[cite: 1]
):
    """Registers a new vehicle. Enforces unique registration rules."""
    # Enforce uniqueness restriction[cite: 1]
    existing = db.query(Vehicle).filter(Vehicle.registration_number == payload.registration_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vehicle with registration number '{payload.registration_number}' already exists."
        )
    
    new_vehicle = Vehicle(**payload.model_dump())
    db.add(new_vehicle)
    db.commit()
    db.refresh(new_vehicle)
    return new_vehicle

# ==========================================
# 2. READ ALL VEHICLES (With Smart Filters)
# ==========================================
@router.get("", response_model=List[VehicleResponse])
def get_vehicles(
    status: Optional[str] = Query(None, description="Filter by status: Available, On Trip, In Shop, Retired"),
    vehicle_type: Optional[str] = Query(None, description="Filter by structural vehicle type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all vehicle entries with clean filtering layers."""
    query = db.query(Vehicle)
    if status:
        query = query.filter(Vehicle.status == status)
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)
        
    return query.all()

# ==========================================
# 3. READ SINGLE VEHICLE
# ==========================================
@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle(
    vehicle_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetches a specific vehicle tracking record by index ID."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    return vehicle

# ==========================================
# 4. UPDATE VEHICLE
# ==========================================
@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int, 
    payload: VehicleUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modifies an existing vehicle registry dataset dynamically."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
    
    # Process modifications mapping update attributes
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vehicle, key, value)
        
    db.commit()
    db.refresh(vehicle)
    return vehicle

# ==========================================
# 5. DELETE VEHICLE
# ==========================================
@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Permanently deletes a target tracking vehicle from the active pool."""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found.")
        
    db.delete(vehicle)
    db.commit()
    return None