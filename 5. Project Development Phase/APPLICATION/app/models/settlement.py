from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import Integer, Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from .loan import Loan

class SettlementPrediction(Base):
    __tablename__ = "settlement_prediction"

    settlement_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.loan_id"), nullable=False)
    suggested_settlement: Mapped[float] = mapped_column(Float, default=0.0)
    risk_category: Mapped[str] = mapped_column(String, default="Low")
    predicted_amount: Mapped[float] = mapped_column(Float, default=0.0)

    loan: Mapped["Loan"] = relationship("Loan", back_populates="settlement_predictions")
