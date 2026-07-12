from pydantic import BaseModel, Field
from typing import Optional

class VehicleBase(BaseModel):
    registration_number: str = Field(..., description="Unique license plate registry code")
    model: str
    vehicle_type: str
    max_load_capacity: float = Field(..., gt=0, description="Maximum operational cargo weight in kg")
    odometer: float = Field(..., ge=0)
    acquisition_cost: float = Field(..., gt=0)
    status: str = Field(default="Available", description="Available, On Trip, In Shop, Retired")

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    model: Optional[str] = None
    vehicle_type: Optional[str] = None
    max_load_capacity: Optional[float] = None
    odometer: Optional[float] = None
    acquisition_cost: Optional[float] = None
    status: Optional[str] = None

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True