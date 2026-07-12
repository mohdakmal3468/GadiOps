from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.schemas.trip import TripCreate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.expense import FuelLog  # Assumes a matching FuelLog DB model is built next
from app.schemas.trip import TripCompletePayload

class TripService:
    # ... (Keep your existing create_and_validate_trip function here) ...

    @staticmethod
    def dispatch_trip(db: Session, trip_id: int) -> Trip:
        """Transitions a trip to 'Dispatched' and updates both assets to 'On Trip'."""
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip record not found.")
        
        if trip.status != "Draft":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only 'Draft' trips can be dispatched.")

        vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
        driver = db.query(Driver).filter(Driver.id == trip.driver_id).first()

        # Final sanity check on asset availability right at dispatch execution
        if vehicle.status != "Available" or driver.status != "Available":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vehicle or Driver is no longer 'Available'.")

        # Atomic State Transitions
        trip.status = "Dispatched"
        vehicle.status = "On Trip"
        driver.status = "On Trip"

        db.commit()
        db.refresh(trip)
        return trip

    @staticmethod
    def complete_trip(db: Session, trip_id: int, payload: TripCompletePayload) -> Trip:
        """Completes a trip, validates/saves the odometer update, creates a fuel log, and marks assets 'Available'."""
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip record not found.")

        if trip.status != "Dispatched":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only actively 'Dispatched' trips can be completed.")

        vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
        driver = db.query(Driver).filter(Driver.id == trip.driver_id).first()

        # Odometer Validation Safeguard
        if payload.final_odometer < vehicle.odometer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid odometer reading. Final odometer ({payload.final_odometer}) cannot be less than the starting value ({vehicle.odometer})."
            )

        # 1. Update vehicle metrics and reset status
        vehicle.odometer = payload.final_odometer
        vehicle.status = "Available"
        
        # 2. Reset driver status
        driver.status = "Available"
        
        # 3. Finalize trip status
        trip.status = "Completed"

        # 4. Automatically generate a matching Fuel & Expense Log entry for operational calculations
        # (This implements example step 6 & 9 from the prompt rules)
        from app.models.expense import FuelLog  # Imported locally to avoid potential cyclic dependency problems
        fuel_entry = FuelLog(
            vehicle_id=vehicle.id,
            trip_id=trip.id,
            liters=payload.fuel_consumed_liters,
            cost=payload.fuel_total_cost,
            date=date.today()
        )
        db.add(fuel_entry)

        db.commit()
        db.refresh(trip)
        return trip

    @staticmethod
    def cancel_trip(db: Session, trip_id: int) -> Trip:
        """Cancels a trip, handling the transition smoothly whether it is a Draft or actively Dispatched."""
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip record not found.")

        if trip.status not in ["Draft", "Dispatched"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot cancel a trip that is already '{trip.status}'.")

        vehicle = db.query(Vehicle).filter(Vehicle.id == trip.vehicle_id).first()
        driver = db.query(Driver).filter(Driver.id == trip.driver_id).first()

        # Revert assets safely back to the pool if it was actively running
        if trip.status == "Dispatched":
            if vehicle: vehicle.status = "Available"
            if driver: driver.status = "Available"

        trip.status = "Cancelled"
        
        db.commit()
        db.refresh(trip)
        return trip

class TripService:
    
    @staticmethod
    def create_and_validate_trip(db: Session, payload: TripCreate) -> Trip:
        """
        Enforces strict compliance validation rules on vehicles, drivers, 
        and weight constraints before creating a Trip record in a Draft state[cite: 1].
        """
        # 1. Fetch matching vehicle asset
        vehicle = db.query(Vehicle).filter(Vehicle.id == payload.vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=status.HTTP_444_NOT_FOUND, detail="Assigned vehicle not found.")
            
        # 2. Fetch matching driver profile
        driver = db.query(Driver).filter(Driver.id == payload.driver_id).first()
        if not driver:
            raise HTTPException(status_code=status.HTTP_444_NOT_FOUND, detail="Assigned driver profile not found.")

        # Business Rule 1: Cargo Weight must not exceed the vehicle's maximum load capacity[cite: 1].
        if payload.cargo_weight > vehicle.max_load_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cargo weight ({payload.cargo_weight}kg) exceeds maximum vehicle payload capacity ({vehicle.max_load_capacity}kg)."
            )

        # Business Rule 2: Retired or In Shop vehicles must never be selected; status must be 'Available'[cite: 1].
        if vehicle.status != "Available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle is unavailable for assignment. Current status: '{vehicle.status}'."
            )

        # Business Rule 3: Drivers with expired licenses or Suspended/Off-Duty status cannot be assigned[cite: 1].
        if driver.status != "Available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Driver is currently unavailable. Status: '{driver.status}'."
            )
            
        if driver.license_expiry_date < date.today():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Driver compliance check failed: Commercial driving license expired on {driver.license_expiry_date}."
            )

        # 3. Everything is safe -> persist the Trip as 'Draft'
        new_trip = Trip(**payload.model_dump(), status="Draft")
        db.add(new_trip)
        db.commit()
        db.refresh(new_trip)
        return new_trip