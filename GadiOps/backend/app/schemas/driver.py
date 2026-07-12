from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class DriverBase(BaseModel):
    name: str
    license_number: str
    license_category: str
    license_expiry_date: date
    contact_number: str
    safety_score: float = Field(default=100.0, ge=0, le=100)
    status: str = Field(default="Available", description="Available, On Trip, Off Duty, Suspended")

class DriverCreate(DriverBase):
    pass

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    license_number: Optional[str] = None
    license_category: Optional[str] = None
    license_expiry_date: Optional[date] = None
    contact_number: Optional[str] = None
    safety_score: Optional[float] = None
    status: Optional[str] = None

class DriverResponse(DriverBase):
    id: int

    class Config:
        from_attributes = True