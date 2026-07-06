from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .user import User

class FinancialProfile(Base):
    __tablename__ = "financial_profile"

    profile_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    emi_ratio: Mapped[float] = mapped_column(Float, default=0.0)
    dti_ratio: Mapped[float] = mapped_column(Float, default=0.0)
    monthly_surplus: Mapped[float] = mapped_column(Float, default=0.0)
    stress_level: Mapped[str] = mapped_column(String, default="Low")

    user: Mapped["User"] = relationship("User", back_populates="financial_profile")
