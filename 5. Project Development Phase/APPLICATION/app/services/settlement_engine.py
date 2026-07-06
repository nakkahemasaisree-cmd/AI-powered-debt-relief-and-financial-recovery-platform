from typing import List

def calculate_settlement_probability(user, loans) -> List[dict]:
    if user.monthly_income > 0:
        emi_ratio = sum(l.emi for l in loans) / user.monthly_income * 100
        total_outstanding = sum(l.outstanding_amount for l in loans)
        debt_to_income = total_outstanding / user.monthly_income * 100
    else:
        emi_ratio = 0.0
        debt_to_income = 0.0

    results = []
    for loan in loans:
        base_settlement = 50.0
        risk_score = 0

        if loan.overdue_months > 0:
            base_settlement += 5
            risk_score += 20
        if emi_ratio > 50:
            base_settlement += 5
            risk_score += 15
        if loan.interest_rate > 12:
            base_settlement += 5
            risk_score += 10
        if debt_to_income > 80:
            base_settlement += 5
            risk_score += 15

        settlement_pct = max(40.0, min(75.0, base_settlement))
        risk_category = "High" if risk_score >= 40 else "Medium" if risk_score >= 20 else "Low"

        results.append({
            "loan_id": loan.loan_id,
            "lender_name": loan.lender_name,
            "outstanding_amount": loan.outstanding_amount,
            "interest_rate": loan.interest_rate,
            "emi": loan.emi,
            "suggested_settlement_percentage": round(settlement_pct, 2),
            "risk_score": risk_score,
            "risk_category": risk_category,
            "predicted_amount": round(loan.outstanding_amount * (settlement_pct / 100), 2),
        })
    return results
