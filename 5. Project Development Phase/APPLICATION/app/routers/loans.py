from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.loan import Loan
from app.schemas.loan import LoanCreate, LoanResponse

router = APIRouter(tags=["loans"])

@router.post("/add-loan", response_model=LoanResponse)
def add_loan(
    loan_data: LoanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loan = Loan(
            user_id=current_user.id,
            lender_name=loan_data.lender_name,
            loan_type=loan_data.loan_type,
            outstanding_amount=loan_data.outstanding_amount,
            interest_rate=loan_data.interest_rate,
            emi=loan_data.emi,
            overdue_months=loan_data.overdue_months,
        )
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to add loan")

@router.get("/loans", response_model=List[LoanResponse])
def get_loans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return db.query(Loan).filter(Loan.user_id == current_user.id).all()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to retrieve loans")

@router.delete("/delete-loan/{loan_id}")
def delete_loan(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loan = db.query(Loan).filter(Loan.loan_id == loan_id, Loan.user_id == current_user.id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        db.delete(loan)
        db.commit()
        return {"message": "Loan deleted successfully"}
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete loan")
