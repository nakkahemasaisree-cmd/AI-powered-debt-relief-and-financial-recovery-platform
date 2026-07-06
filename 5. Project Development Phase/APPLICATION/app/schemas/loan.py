from pydantic import BaseModel

class LoanCreate(BaseModel):
    lender_name: str
    loan_type: str
    outstanding_amount: float
    interest_rate: float
    emi: float
    overdue_months: int = 0

class LoanResponse(BaseModel):
    loan_id: int
    user_id: int
    lender_name: str
    loan_type: str
    outstanding_amount: float
    interest_rate: float
    emi: float
    overdue_months: int

    class Config:
        from_attributes = True
