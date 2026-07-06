from fastapi import APIRouter, Depends, HTTPException  # type: ignore[import]
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.auth import get_current_user
from app.models.user import User
from app.models.loan import Loan
from app.models.ai_models import AINegotiation, AIHistory
from app.services.financial_engine import calculate_financial_health
from app.services.settlement_engine import calculate_settlement_probability
from app.services.ai_engine import generate_negotiation_strategy, generate_negotiation_letter

router = APIRouter(tags=["ai"])

@router.get("/settlement-predictor")
def settlement_predictor(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        if not loans:
            return {"settlements": [], "message": "No loans found"}
        return {"settlements": calculate_settlement_probability(current_user, loans)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Settlement predictor error: {str(e)}")

@router.get("/ai-negotiation-strategy")
def ai_negotiation_strategy(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        if not loans:
            return {"strategy": "No loans found to generate strategy"}
        health = calculate_financial_health(current_user, loans)
        settlement_data = calculate_settlement_probability(current_user, loans)
        strategy = generate_negotiation_strategy(current_user, loans, health, settlement_data)
        db.add(AIHistory(
            user_id=current_user.id,
            generated_content=strategy,
            query_type="Negotiation Strategy",
            timestamp=datetime.utcnow(),
        ))
        db.commit()
        return {"strategy": strategy, "financial_health": health, "settlement_data": settlement_data}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"AI strategy error: {str(e)}")

@router.get("/generate-negotiation-email/{loan_id}")
def generate_negotiation_email(
    loan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        loan = db.query(Loan).filter(
            Loan.loan_id == loan_id, Loan.user_id == current_user.id
        ).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        health = calculate_financial_health(current_user, loans)
        settlement_data = calculate_settlement_probability(current_user, loans)
        strategy = generate_negotiation_strategy(current_user, loans, health, settlement_data)
        letter = generate_negotiation_letter(current_user, loan, strategy)
        db.add(AINegotiation(
            loan_id=loan.loan_id, user_id=current_user.id,
            negotiation_strategy=strategy, negotiation_letter=letter,
            generated_date=datetime.utcnow(),
        ))
        db.add(AIHistory(
            user_id=current_user.id, generated_content=letter,
            query_type="Negotiation Letter", timestamp=datetime.utcnow(),
        ))
        db.commit()
        return {"loan_id": loan_id, "lender_name": loan.lender_name, "letter": letter, "strategy": strategy}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Email generation error: {str(e)}")

@router.get("/ai-history")
def get_ai_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        history = (
            db.query(AIHistory)
            .filter(AIHistory.user_id == current_user.id)
            .order_by(AIHistory.timestamp.desc())
            .limit(50).all()
        )
        return {
            "history": [
                {
                    "history_id": h.history_id,
                    "query_type": h.query_type,
                    "generated_content": h.generated_content,
                    "timestamp": h.timestamp.isoformat() if h.timestamp else None,
                }
                for h in history
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History error: {str(e)}")
