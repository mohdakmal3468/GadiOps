from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.vehicle import Vehicle
from app.models.trip import Trip
from app.models.expense import FuelLog, MaintenanceLog, Expense

import csv
import io
from sqlalchemy.orm import Session
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.models.driver import Driver

class AnalyticsService:
    # ... (Keep your existing dashboard and ROI math methods here) ...

    @staticmethod
    def export_trips_to_csv_string(db: Session) -> str:
        """
        Queries all system transport operations logs and formats them 
        into a lightweight tabular CSV string for client downloads.
        """
        # Fetch operational data joined with reference tables for richer reports
        trips = db.query(Trip).all()

        # Initialize an in-memory string buffer
        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)

        # 1. Write the Tabular Header Row
        writer.writerow([
            "Trip ID", "Source", "Destination", "Cargo Weight (kg)", 
            "Planned Distance (km)", "Lifecycle Status", "Vehicle ID", "Driver ID"
        ])

        # 2. Iterate and append raw tracking rows
        for trip in trips:
            writer.writerow([
                trip.id,
                trip.source,
                trip.destination,
                trip.cargo_weight,
                trip.planned_distance,
                trip.status,
                trip.vehicle_id,
                trip.driver_id
            ])

        return output.getvalue()

@staticmethod
def calculate_vehicle_roi(db: Session, vehicle_id: int) -> dict:
        """
        Calculates financial ROI for an individual tracking asset based on the strict formula:
        ROI = (Revenue - (Maintenance + Fuel)) / Acquisition Cost
        """
        # 1. Gather the foundational asset information
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            return {"error": "Vehicle registry reference not found"}

        # 2. Extract aggregate financial layers
        total_revenue = db.query(func.sum(Trip.revenue)).filter(
            Trip.vehicle_id == vehicle_id, 
            Trip.status == "Completed"
        ).scalar() or 0.0

        total_fuel = db.query(func.sum(FuelLog.cost)).filter(
            FuelLog.vehicle_id == vehicle_id
        ).scalar() or 0.0

        total_maintenance = db.query(func.sum(MaintenanceLog.cost)).filter(
            MaintenanceLog.vehicle_id == vehicle_id
        ).scalar() or 0.0

        # 3. Compute the strict ROI Formula
        acquisition_cost = vehicle.acquisition_cost
        net_profit = total_revenue - (total_maintenance + total_fuel)
        
        # Guard against zero-division errors if sample dataset has bad data
        roi_ratio = 0.0
        if acquisition_cost > 0:
            roi_ratio = net_profit / acquisition_cost

        return {
            "vehicle_id": vehicle.id,
            "registration_number": vehicle.registration_number,
            "acquisition_cost": acquisition_cost,
            "total_revenue": total_revenue,
            "total_fuel_cost": total_fuel,
            "total_maintenance_cost": total_maintenance,
            "net_operational_profit": net_profit,
            "roi_ratio": round(roi_ratio, 4),               # Format for backend calculations (e.g., 0.1452)
            "roi_percentage": f"{round(roi_ratio * 100, 2)}%", # Format for easier front-end presentation (e.g., "14.52%")
        }

class AnalyticsService:

    @staticmethod
    def get_dashboard_metrics(db: Session) -> dict:
        """
        Gathers database counts and calculates fleet utilization percentages.
        """
        # 1. Fetch total counts of vehicles split by status
        available_vehicles = db.query(Vehicle).filter(Vehicle.status == "Available").count()
        on_trip_vehicles = db.query(Vehicle).filter(Vehicle.status == "On Trip").count()
        in_shop_vehicles = db.query(Vehicle).filter(Vehicle.status == "In Shop").count()
        retired_vehicles = db.query(Vehicle).filter(Vehicle.status == "Retired").count()
        
        total_active_fleet = available_vehicles + on_trip_vehicles + in_shop_vehicles
        
        # 2. Additional Prompt KPIs: Trips and Drivers
        active_trips = db.query(Trip).filter(Trip.status == "Dispatched").count()
        pending_trips = db.query(Trip).filter(Trip.status == "Draft").count()
        drivers_on_duty = db.query(Driver).filter(Driver.status == "On Trip").count()

        # 3. Calculate Fleet Utilization (%) Formula
        # Utilization (%) = (Vehicles On Trip / Total Non-Retired Fleet) * 100
        fleet_utilization_pct = 0.0
        if total_active_fleet > 0:
            fleet_utilization_pct = round((on_trip_vehicles / total_active_fleet) * 100, 2)

        return {
            "active_vehicles": on_trip_vehicles, # Current vehicles out on operations
            "available_vehicles": available_vehicles,
            "vehicles_in_maintenance": in_shop_vehicles,
            "retired_vehicles": retired_vehicles,
            "active_trips": active_trips,
            "pending_trips": pending_trips,
            "drivers_on_duty": drivers_on_duty,
            "fleet_utilization_percentage": fleet_utilization_pct
        }