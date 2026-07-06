from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    monthly_income: float = 0.0
    monthly_expenses: float = 0.0
    lump_sum_available: float = 0.0

class UserUpdate(BaseModel):
    monthly_income: Optional[float] = None
    monthly_expenses: Optional[float] = None
    lump_sum_available: Optional[float] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    monthly_income: float
    monthly_expenses: float
    lump_sum_available: float

    class Config:
        from_attributes = True
