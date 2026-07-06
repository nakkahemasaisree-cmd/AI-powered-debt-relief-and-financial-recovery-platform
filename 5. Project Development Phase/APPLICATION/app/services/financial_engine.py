from typing import List

def calculate_financial_health(user, loans) -> dict:
    total_emi = sum(loan.emi for loan in loans)
    total_outstanding = sum(loan.outstanding_amount for loan in loans)
    surplus = user.monthly_income - user.monthly_expenses - total_emi

    if user.monthly_income > 0:
        emi_ratio = (total_emi / user.monthly_income) * 100
        debt_to_income = (total_outstanding / user.monthly_income) * 100
    else:
        emi_ratio = 0.0
        debt_to_income = 0.0

    if emi_ratio > 50:
        stress_level = "High"
    elif emi_ratio >= 30:
        stress_level = "Medium"
    else:
        stress_level = "Low"

    return {
        "total_emi": round(total_emi, 2),
        "total_outstanding": round(total_outstanding, 2),
        "surplus": round(surplus, 2),
        "emi_ratio_percent": round(emi_ratio, 2),
        "debt_to_income_percent": round(debt_to_income, 2),
        "stress_level": stress_level,
        "total_loans": len(loans),
    }

def calculate_loan_priority(loans, emi_ratio: float = 0) -> list:
    prioritized = []
    for loan in loans:
        is_overdue = loan.overdue_months > 0
        high_interest = loan.interest_rate > 12
        high_emi_ratio = emi_ratio > 50

        if is_overdue or high_interest or high_emi_ratio:
            priority = "High"
        elif loan.interest_rate > 8 or loan.overdue_months > 0:
            priority = "Medium"
        else:
            priority = "Low"

        prioritized.append({
            "loan_id": loan.loan_id,
            "lender_name": loan.lender_name,
            "loan_type": loan.loan_type,
            "outstanding_amount": loan.outstanding_amount,
            "interest_rate": loan.interest_rate,
            "emi": loan.emi,
            "overdue_months": loan.overdue_months,
            "priority": priority,
        })

    order = {"High": 0, "Medium": 1, "Low": 2}
    prioritized.sort(key=lambda x: order[x["priority"]])
    return prioritized

def simulate_debt_timeline(user, loans, extra_payment: float = 0) -> dict:
    balances = {loan.loan_id: loan.outstanding_amount for loan in loans}
    rates = {loan.loan_id: loan.interest_rate / 100 / 12 for loan in loans}
    emis = {loan.loan_id: loan.emi for loan in loans}

    timeline_preview = []
    months = 0

    while any(b > 0 for b in balances.values()) and months < 240:
        months += 1
        largest = max(balances, key=lambda lid: balances[lid]) if balances else None
        extra_applied = False

        for loan_id in list(balances.keys()):
            if balances[loan_id] <= 0:
                continue
            interest = balances[loan_id] * rates[loan_id]
            payment = emis[loan_id]
            if not extra_applied and loan_id == largest and extra_payment > 0:
                payment += extra_payment
                extra_applied = True
            balances[loan_id] = max(0, balances[loan_id] + interest - payment)

        if months <= 12:
            timeline_preview.append({"month": months, "total_remaining": round(sum(balances.values()), 2)})

    final_remaining = round(sum(balances.values()), 2)
    return {
        "months_to_debt_free": months if final_remaining == 0 else None,
        "final_remaining_balance": final_remaining,
        "timeline_preview": timeline_preview,
    }
