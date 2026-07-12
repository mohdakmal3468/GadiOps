from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.trip import TripCreate, TripResponse
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.services.trip_service import TripService
from app.models.user import User

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.trip import TripResponse, TripCompletePayload
from app.services.trip_service import TripService
from app.models.user import User

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.schemas.trip import TripCreate, TripResponse, TripCompletePayload
from app.services.trip_service import TripService
from app.models.trip import Trip
from app.models.user import User

router = APIRouter(prefix="/trips", tags=["Trip Operations Management"])

# ==========================================
# 1. CREATE TRIP (POST /api/trips)
# ==========================================
@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    payload: TripCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Validates parameters and initiates a new transport operation workflow in 'Draft' state[cite: 1].
    """
    return TripService.create_and_validate_trip(db, payload)


# ==========================================
# 2. LIST TRIPS (GET /api/trips)
# ==========================================
@router.get("", response_model=List[TripResponse])
def list_trips(
    status: Optional[str] = Query(None, description="Filter trips by status: Draft, Dispatched, Completed, Cancelled[cite: 1]"),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Lists all historical and ongoing transport operations logs with an optional status filter[cite: 1].
    """
    query = db.query(Trip)
    if status:
        query = query.filter(Trip.status == status.capitalize())
    return query.all()


# ==========================================
# 3. TRANSITION WORKFLOW (POST /api/trips/{trip_id}/transition)
# ==========================================
@router.post("/{trip_id}/transition", response_model=TripResponse)
def transition_trip_status(
    trip_id: int, 
    target_status: str = Query(..., description="Target status transition: Dispatched, Completed, Cancelled[cite: 1]"),
    complete_payload: Optional[TripCompletePayload] = None, # Required only when completing a trip[cite: 1]
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    A unified lifecycle interface handling structural state machine mutations[cite: 1].
    Expects target_status query parameter to route into matching business services[cite: 1].
    """
    action = target_status.lower()

    if action == "dispatched":
        return TripService.dispatch_trip(db, trip_id)

    elif action == "completed":
        if not complete_payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Completing a trip requires odometer readings and fuel consumption data arrays[cite: 1]."
            )
        return TripService.complete_trip(db, trip_id, complete_payload)

    elif action == "cancelled":
        return TripService.cancel_trip(db, trip_id)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid workflow transition variant: '{target_status}'. Use Dispatched, Completed, or Cancelled[cite: 1]."
        )

# ... (Keep your base POST create and GET list routes here) ...
@router.post("/{trip_id}/dispatch", response_model=TripResponse)
def dispatch_operation(trip_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Transitions a selected workflow card to 'Dispatched' and locks down assets."""
    return TripService.dispatch_trip(db, trip_id)

@router.post("/{trip_id}/complete", response_model=TripResponse)
def complete_operation(trip_id: int, payload: TripCompletePayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Folds operational values back into data aggregates, unlocks assets, and closes active trip entries."""
    return TripService.complete_trip(db, trip_id, payload)

@router.post("/{trip_id}/cancel", response_model=TripResponse)
def cancel_operation(trip_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Reverts assigned resources back to active pools instantly and drops the task track."""
    return TripService.cancel_trip(db, trip_id)

@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(payload: TripCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Validates parameters and initiates a new transport operation workflow[cite: 1]."""
    return TripService.create_and_validate_trip(db, payload)

@router.post("/{trip_id}/transition", response_model=TripResponse)
def transition_trip_status(
    trip_id: int, 
    target_status: str, # Expecting: Dispatched, Completed, Cancelled
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handles status changes and auto-updates vehicle and driver resources[cite: 1]."""
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=status.HTTP_444_NOT_FOUND, detail="Trip record tracking number not found.")
        
    vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
    driver = db.query(Driver).filter(Driver.id == trip.driver_id).first()
    
    normalized_status = target_status.capitalize()

    # Rule Workflow A: Dispatching an active run changes assets to 'On Trip'[cite: 1]
    if normalized_status == "Dispatched":
        if trip.status != "Draft":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only Draft entries can be dispatched.")
        trip.status = "Dispatched"
        vehicle.status = "On Trip"
        driver.status = "On Trip"

    # Rule Workflow B: Completing a run returns assets to 'Available'[cite: 1]
    elif normalized_status == "Completed":
        if trip.status != "Dispatched":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only active Dispatched trips can be completed.")
        trip.status = "Completed"
        vehicle.status = "Available"
        driver.status = "Available"

    # Rule Workflow C: Cancelling an active trip returns assets to 'Available'[cite: 1]
    elif normalized_status == "Cancelled":
        if trip.status not in ["Draft", "Dispatched"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot cancel finalized trips.")
        trip.status = "Cancelled"
        vehicle.status = "Available"
        driver.status = "Available"
        
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid target workflow lifecycle node.")

    db.commit()
    db.refresh(trip)
    return trip

@router.get("", response_model=List[TripResponse])
def list_trips(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Lists all historical and ongoing transport operations logs."""
    return db.query(Trip).all()