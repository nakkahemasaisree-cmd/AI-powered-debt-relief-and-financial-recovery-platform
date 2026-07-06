from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base

if TYPE_CHECKING:
    from .loan import Loan
    from .user import User

class AINegotiation(Base):
    __tablename__ = "ai_negotiation"

    ai_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    loan_id: Mapped[int] = mapped_column(ForeignKey("loans.loan_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    negotiation_strategy: Mapped[Optional[str]] = mapped_column(Text)
    negotiation_letter: Mapped[Optional[str]] = mapped_column(Text)
    generated_date: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())

    loan: Mapped["Loan"] = relationship("Loan", back_populates="ai_negotiations")

class AIHistory(Base):
    __tablename__ = "ai_history"

    history_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    generated_content: Mapped[Optional[str]] = mapped_column(Text)
    query_type: Mapped[Optional[str]] = mapped_column(String)
    timestamp: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="ai_history")
