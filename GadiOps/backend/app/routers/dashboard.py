from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.services.analytics_service import AnalyticsService
from app.models.user import User

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers.auth import get_current_user
from app.services.analytics_service import AnalyticsService
from app.models.vehicle import Vehicle
from app.models.user import User

# ... (Keep your base /stats route here) ...

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.core.database import get_db
from app.routers.auth import get_current_user
from app.services.analytics_service import AnalyticsService
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard Aggregates"])

# ... (Keep your base /stats and /fleet-roi routes here) ...

@router.get("/export/csv")
def download_operational_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generates and streams a downloadable CSV report of all fleet operations[cite: 1].
    """
    # Role-Based Guard: Restrict data exporting to authoritative managers/analysts
    if current_user.role not in ["Fleet Manager", "Financial Analyst"]:
        raise HTTPException(status_code=403, detail="Unauthorized export permissions profile.")

    # Generate the string data
    csv_data = AnalyticsService.export_trips_to_csv_string(db)
    
    # Convert string data into a streaming byte buffer
    response_stream = io.BytesIO(csv_data.encode("utf-8"))
    
    # Return streaming payload with explicit browser download disposition instructions
    return StreamingResponse(
        response_stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=GadiOps_Operational_Report.csv"}
    )

@router.get("/fleet-roi")
def get_fleet_roi_breakdown(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Returns an analytical matrix calculation outlining the precise ROI metrics for all non-retired fleet vehicles[cite: 1].
    """
    # Role-Based Security: Keep vehicle profit hidden from standard drivers if desired[cite: 1]
    if current_user.role not in ["Fleet Manager", "Financial Analyst"]:
         raise HTTPException(status_code=403, detail="Unauthorized role permission access path.")

    vehicles = db.query(Vehicle).filter(Vehicle.status != "Retired").all()
    roi_report = [AnalyticsService.calculate_vehicle_roi(db, v.id) for v in vehicles]
    
    return roi_report

@router.get("/stats")
def get_fleet_statistics(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Returns an aggregated payload containing fleet statuses and utilization KPIs[cite: 1].
    """
    return AnalyticsService.get_dashboard_metrics(db)