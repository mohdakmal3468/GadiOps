from pydantic import BaseModel, Field
from typing import Optional

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