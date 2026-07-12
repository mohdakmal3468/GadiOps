from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverUpdate, DriverResponse
from app.models.user import User

router = APIRouter(prefix="/drivers", tags=["Driver Management"])

# ==========================================
# 1. CREATE DRIVER
# ==========================================
@router.post("", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(
    payload: DriverCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Registers a new fleet driver profile."""
    existing = db.query(Driver).filter(Driver.license_number == payload.license_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Driver with license number '{payload.license_number}' already exists."
        )
    
    new_driver = Driver(**payload.model_dump())
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver

# ==========================================
# 2. READ ALL DRIVERS (With Filtering layers)
# ==========================================
@router.get("", response_model=List[DriverResponse])
def get_drivers(
    status: Optional[str] = Query(None, description="Filter by: Available, On Trip, Off Duty, Suspended"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieves all driver registries with smart optional filtering options."""
    query = db.query(Driver)
    if status:
        query = query.filter(Driver.status == status)
        
    return query.all()

# ==========================================
# 3. READ SINGLE DRIVER
# ==========================================
@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(
    driver_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Fetches details for a specific operational driver by profile ID."""
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found.")
    return driver

# ==========================================
# 4. UPDATE DRIVER PROFILE
# ==========================================
@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int, 
    payload: DriverUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Modifies structural datasets inside a driver profile resource."""
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found.")
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(driver, key, value)
        
    db.commit()
    db.refresh(driver)
    return driver

# ==========================================
# 5. DELETE DRIVER PROFILE
# ==========================================
@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(
    driver_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deletes an operational driver profile permanently from the active directory."""
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    if not driver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Driver profile not found.")
        
    db.delete(driver)
    db.commit()
    db.refresh(driver)
    return None