from __future__ import annotations
from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .ai_models import AINegotiation
    from .settlement import SettlementPrediction
    from .user import User

class Loan(Base):
    __tablename__ = "loans"

    loan_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    lender_name: Mapped[str] = mapped_column(String, nullable=False)
    loan_type: Mapped[str] = mapped_column(String, nullable=False)
    outstanding_amount: Mapped[float] = mapped_column(Float, nullable=False)
    interest_rate: Mapped[float] = mapped_column(Float, nullable=False)
    emi: Mapped[float] = mapped_column(Float, nullable=False)
    overdue_months: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship("User", back_populates="loans")
    settlement_predictions: Mapped[List["SettlementPrediction"]] = relationship(
        "SettlementPrediction", back_populates="loan", cascade="all, delete-orphan"
    )
    ai_negotiations: Mapped[List["AINegotiation"]] = relationship(
        "AINegotiation", back_populates="loan", cascade="all, delete-orphan"
    )
