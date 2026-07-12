from pydantic import BaseModel, Field
from datetime import date as dt_date
from typing import Optional

# Fuel Schemas
class FuelLogCreate(BaseModel):
    vehicle_id: int
    trip_id: Optional[int] = None
    liters: float = Field(..., gt=0)
    cost: float = Field(..., gt=0)
    date: dt_date = Field(default_factory=dt_date.today)

class FuelLogResponse(FuelLogCreate):
    id: int
    class Config:
        from_attributes = True

# Miscellaneous Expense Schemas
class ExpenseCreate(BaseModel):
    vehicle_id: int
    category: str = Field(..., description="Tolls, Permits, Insurance, etc.")
    cost: float = Field(..., gt=0)
    date: dt_date = Field(default_factory=dt_date.today)
    description: Optional[str] = None

class ExpenseResponse(ExpenseCreate):
    id: int
    class Config:
        from_attributes = True