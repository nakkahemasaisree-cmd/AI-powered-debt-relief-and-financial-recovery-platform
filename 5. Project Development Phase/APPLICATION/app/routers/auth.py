import logging
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserRegister, UserResponse
from app.auth import create_access_token
from app.services.email_service import send_registration_email, send_login_notification

logger = logging.getLogger(__name__)
router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == user_data.email.strip().lower()).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed = generate_password_hash(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email.strip().lower(),
            password=hashed,
            monthly_income=user_data.monthly_income,
            monthly_expenses=user_data.monthly_expenses,
            lump_sum_available=user_data.lump_sum_available,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        # send registration email in background (will no-op if SMTP not configured)
        try:
            background_tasks.add_task(send_registration_email, user.email, user.name)
        except Exception:
            logger.exception("Failed to schedule registration email")
        return user
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), background_tasks: BackgroundTasks = None):
    try:
        user = db.query(User).filter(User.email == form_data.username.strip().lower()).first()
        if not user:
            logger.warning(f"Login failed: user not found for email {form_data.username}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not check_password_hash(user.password, form_data.password):
            logger.warning(f"Login failed: password mismatch for email {form_data.username}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token(data={"sub": user.email})
        try:
            if background_tasks:
                background_tasks.add_task(send_login_notification, user.email, user.name)
        except Exception:
            logger.exception("Failed to schedule login notification email")
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Login failed")

@router.get("/debug-user")
def debug_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email.strip().lower()).first()
    if not user:
        return {"found": False}
    return {"found": True, "id": user.id, "name": user.name, "email": user.email}
