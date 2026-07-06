from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .ai_models import AIHistory
    from .financial_profile import FinancialProfile
    from .loan import Loan

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    monthly_income: Mapped[float] = mapped_column(Float, default=0.0)
    monthly_expenses: Mapped[float] = mapped_column(Float, default=0.0)
    lump_sum_available: Mapped[float] = mapped_column(Float, default=0.0)

    loans: Mapped[List["Loan"]] = relationship("Loan", back_populates="user", cascade="all, delete-orphan")
    financial_profile: Mapped[Optional["FinancialProfile"]] = relationship(
        "FinancialProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    ai_history: Mapped[List["AIHistory"]] = relationship("AIHistory", back_populates="user", cascade="all, delete-orphan")
