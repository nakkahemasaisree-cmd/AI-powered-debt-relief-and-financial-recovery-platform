from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse

router = APIRouter(tags=["profile"])

@router.put("/update-profile", response_model=UserResponse)
def update_profile(
    update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        if update.monthly_income is not None:
            current_user.monthly_income = update.monthly_income
        if update.monthly_expenses is not None:
            current_user.monthly_expenses = update.monthly_expenses
        if update.lump_sum_available is not None:
            current_user.lump_sum_available = update.lump_sum_available
        db.commit()
        db.refresh(current_user)
        return current_user
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Profile update failed")
