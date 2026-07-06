import os
import logging
import importlib
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

def _call_gemini(prompt: str) -> Optional[str]:
    if not GOOGLE_API_KEY:
        return None
    try:
        genai = importlib.import_module("google.generativeai")
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except (ImportError, ModuleNotFoundError):
        logger.warning("google.generativeai not installed, using fallback strategy")
        return None
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return None

def _fallback_strategy(user, loans, financial_health, settlement_data) -> str:
    stress = financial_health.get("stress_level", "Medium")
    surplus = financial_health.get("surplus", 0)
    emi_ratio = financial_health.get("emi_ratio_percent", 0)
    total_outstanding = financial_health.get("total_outstanding", 0)

    if not settlement_data:
        return "Insufficient loan data to generate strategy."

    best = min(settlement_data, key=lambda x: x.get("risk_score", 0))
    pct = best.get("suggested_settlement_percentage", 50)
    amount = best.get("predicted_amount", 0)
    risk = best.get("risk_category", "Medium")
    plan_type = "Lump Sum Settlement" if user.lump_sum_available >= amount else "Structured Payment Plan"

    return f"""=== AI NEGOTIATION STRATEGY (Rule-Based) ===

FINANCIAL OVERVIEW
  Monthly Income    : ₹{user.monthly_income:,.0f}
  Monthly Surplus   : ₹{surplus:,.0f}
  EMI-to-Income     : {emi_ratio:.1f}%
  Total Outstanding : ₹{total_outstanding:,.0f}
  Debt Stress Level : {stress}

RECOMMENDED APPROACH: {plan_type}
  Settlement Offer  : {pct:.0f}% of outstanding balance
  Estimated Amount  : ₹{amount:,.0f}
  Risk Category     : {risk}

KEY TALKING POINTS
  1. Cite financial hardship and inability to continue full EMI payments
  2. Offer a one-time settlement or structured plan to close the account
  3. Request waiver of penalty interest and late charges
  4. Ask for an NOC (No Objection Certificate) upon settlement
  5. Negotiate credit bureau reporting — request 'Settled' status

LENDER APPROACH
  - Open communication professionally via written letter
  - Document all conversations and keep copies
  - Escalate to senior bank official if initial contact refuses

DOCUMENT CHECKLIST
  [ ] Income proof (salary slips / bank statements — last 3 months)
  [ ] Loan account statement
  [ ] Medical/emergency documents if applicable
  [ ] Written settlement offer letter
  [ ] Identity proof (Aadhaar/PAN)"""

def generate_negotiation_strategy(user, loans, financial_health, settlement_data) -> str:
    if not loans:
        return "No loans found to generate a strategy."

    loan_summary = "\n".join([
        f"- {l.lender_name} | {l.loan_type} | ₹{l.outstanding_amount:,.0f} outstanding | "
        f"{l.interest_rate}% interest | ₹{l.emi:,.0f} EMI | {l.overdue_months} months overdue"
        for l in loans
    ])
    settlement_summary = "\n".join([
        f"- Loan {s['loan_id']} ({s['lender_name']}): {s['suggested_settlement_percentage']}% offer | "
        f"Predicted ₹{s['predicted_amount']:,.0f} | Risk: {s['risk_category']}"
        for s in settlement_data
    ])

    prompt = f"""You are an expert financial debt negotiation advisor. Generate a professional,
detailed negotiation strategy for a borrower with the following profile:

BORROWER PROFILE:
- Name: {user.name}
- Monthly Income: ₹{user.monthly_income:,.0f}
- Monthly Expenses: ₹{user.monthly_expenses:,.0f}
- Monthly Surplus: ₹{financial_health.get('surplus', 0):,.0f}
- Lump Sum Available: ₹{user.lump_sum_available:,.0f}
- EMI-to-Income Ratio: {financial_health.get('emi_ratio_percent', 0):.1f}%
- Debt Stress Level: {financial_health.get('stress_level', 'Unknown')}

LOANS:
{loan_summary}

SETTLEMENT DATA:
{settlement_summary}

Please provide:
1. Financial Overview Summary
2. Recommended Settlement Approach
3. Key Negotiation Talking Points (5 points)
4. Lender-specific Approach Strategy
5. Settlement Offer Percentages per loan
6. Document Checklist
7. Credit Score Recovery Tips

Format clearly with sections and bullet points. Be specific and actionable."""

    result = _call_gemini(prompt)
    if result is None:
        result = _fallback_strategy(user, loans, financial_health, settlement_data)
    return result

def generate_negotiation_letter(user, loan, strategy: str) -> str:
    prompt = f"""Write a formal settlement request letter to a lender.

BORROWER:
- Name: {user.name}
- Email: {user.email}
- Monthly Income: ₹{user.monthly_income:,.0f}
- Lump Sum Available: ₹{user.lump_sum_available:,.0f}

LOAN:
- Lender: {loan.lender_name}
- Type: {loan.loan_type}
- Outstanding: ₹{loan.outstanding_amount:,.0f}
- Rate: {loan.interest_rate}%
- EMI: ₹{loan.emi:,.0f}
- Overdue: {loan.overdue_months} months

Include: subject line, account details, hardship explanation, specific settlement proposal
({int(55)}% of outstanding = ₹{loan.outstanding_amount * 0.55:,.0f}), requested concessions
(penalty waiver, NOC, credit bureau update), professional closing. Indian banking context."""

    result = _call_gemini(prompt)
    if result is None:
        pct = 55
        amount = loan.outstanding_amount * (pct / 100)
        today = datetime.now().strftime("%B %d, %Y")
        result = f"""Subject: Settlement Request for Loan Account – {loan.lender_name}

Date: {today}

To,
The Settlement Officer / Recovery Manager
{loan.lender_name}

Dear Sir/Madam,

Re: One-Time Settlement Request for {loan.loan_type} Loan Account

I, {user.name}, am writing to formally request a one-time settlement for my {loan.loan_type} account with {loan.lender_name}.

ACCOUNT DETAILS:
  Loan Type           : {loan.loan_type}
  Outstanding Balance : ₹{loan.outstanding_amount:,.0f}
  Current EMI         : ₹{loan.emi:,.0f}
  Overdue Months      : {loan.overdue_months}

FINANCIAL HARDSHIP:
Due to unforeseen financial difficulties, I am unable to continue the EMI of ₹{loan.emi:,.0f}. My monthly income is ₹{user.monthly_income:,.0f} with constrained surplus after expenses.

SETTLEMENT PROPOSAL:
I propose ₹{amount:,.0f} ({pct}% of ₹{loan.outstanding_amount:,.0f}), payable within 30 days of written confirmation.

Requested:
  1. Acceptance of settlement amount
  2. Waiver of penalty interest and late charges
  3. No Objection Certificate (NOC) upon payment
  4. Account reported as "Settled" to credit bureaus

Yours faithfully,
{user.name}
Email: {user.email}
Date: {today}

[Enclosures: Income Proof, Identity Proof, Bank Statements — 3 Months]"""
    return result
