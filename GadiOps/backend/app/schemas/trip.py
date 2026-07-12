from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel, Field

class TripCompletePayload(BaseModel):
    final_odometer: float = Field(..., gt=0, description="Ending odometer reading of the vehicle")
    fuel_consumed_liters: float = Field(..., gt=0, description="Total fuel liters used during this specific trip")
    fuel_total_cost: float = Field(..., gt=0, description="Total cost of fuel consumed during this trip")

class TripCreate(BaseModel):
    source: str
    destination: str
    cargo_weight: float = Field(..., gt=0)
    planned_distance: float = Field(..., gt=0)
    vehicle_id: int
    driver_id: int

class TripResponse(TripCreate):
    id: int
    status: str

    class Config:
        from_attributes = True