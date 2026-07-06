from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.loan import Loan
from app.services.financial_engine import (
    calculate_financial_health,
    calculate_loan_priority,
    simulate_debt_timeline,
)

router = APIRouter(tags=["dashboard"])

@router.get("/dashboard-data")
def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        health = calculate_financial_health(current_user, loans)
        prioritized = calculate_loan_priority(loans, health.get("emi_ratio_percent", 0))
        return {
            "user": {
                "id": current_user.id,
                "name": current_user.name,
                "email": current_user.email,
                "monthly_income": current_user.monthly_income,
                "monthly_expenses": current_user.monthly_expenses,
                "lump_sum_available": current_user.lump_sum_available,
            },
            "financial_health": health,
            "loans": prioritized,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dashboard data error: {str(e)}")

@router.get("/financial-health")
def get_financial_health(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        health = calculate_financial_health(current_user, loans)
        return {
            "user": {
                "monthly_income": current_user.monthly_income,
                "monthly_expenses": current_user.monthly_expenses,
                "lump_sum_available": current_user.lump_sum_available,
            },
            **health,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Financial health error: {str(e)}")

@router.get("/debt-timeline")
def get_debt_timeline(
    extra_payment: float = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        return simulate_debt_timeline(current_user, loans, extra_payment)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Timeline error: {str(e)}")
