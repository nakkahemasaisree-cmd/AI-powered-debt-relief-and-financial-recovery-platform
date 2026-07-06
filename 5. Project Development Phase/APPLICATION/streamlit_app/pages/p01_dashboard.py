import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import api_client as api
from components import stat_card, stress_badge, risk_badge, currency
from typing import Any, Dict, List

def show():
    st.markdown("""
    <div class="page-header">
      <h1>Dashboard Overview</h1>
      <p>Your financial snapshot at a glance</p>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading dashboard..."):
        data: Dict[str, Any] = api.get_dashboard_data() or {}

    if not isinstance(data, dict) or "error" in data:
        st.error(f"Failed to load dashboard: {data.get('error', 'Unknown error') if isinstance(data, dict) else 'Invalid response'}")
        return

    user: Dict[str, Any] = data.get("user", {}) if isinstance(data.get("user", {}), dict) else {}
    health: Dict[str, Any] = data.get("financial_health", {}) if isinstance(data.get("financial_health", {}), dict) else {}
    loans: List[Dict[str, Any]] = data.get("loans", []) if isinstance(data.get("loans", []), list) else []

    surplus = health.get("surplus", 0)
    surplus_color = "#ef4444" if surplus < 0 else "#10b981"
    stress = health.get("stress_level", "Low")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(stat_card("Monthly Surplus", currency(surplus), "After EMI & expenses", color=surplus_color), unsafe_allow_html=True)
    with c2:
        st.markdown(stat_card("Total Outstanding", currency(health.get("total_outstanding", 0)), f"{health.get('total_loans', 0)} loans"), unsafe_allow_html=True)
    with c3:
        st.markdown(stat_card("Total EMI/mo", currency(health.get("total_emi", 0)), "Combined monthly"), unsafe_allow_html=True)
    with c4:
        st.markdown(stat_card("Debt-to-Income", f"{health.get('debt_to_income_percent', 0):.1f}%", "Ideal: below 40%"), unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="stat-card"><div class="label">Stress Level</div><div style="margin-top:0.5rem;">{stress_badge(stress)}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    col_profile, col_loans = st.columns([1, 2])

    with col_profile:
        st.markdown("<h3 style=\"font-family:'Syne',sans-serif;font-size:1.1rem;color:#f1f5f9;\">Financial Profile</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="fin-card">
          <div style="margin-bottom:1rem;">
            <div style="font-size:0.75rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;">Monthly Income</div>
            <div style="font-size:1.4rem;font-weight:700;color:#10b981;font-family:'Syne',sans-serif;">{currency(user.get('monthly_income', 0))}</div>
          </div>
          <div style="margin-bottom:1rem;">
            <div style="font-size:0.75rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;">Monthly Expenses</div>
            <div style="font-size:1.4rem;font-weight:700;color:#f1f5f9;font-family:'Syne',sans-serif;">{currency(user.get('monthly_expenses', 0))}</div>
          </div>
          <div>
            <div style="font-size:0.75rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;">Lump Sum Available</div>
            <div style="font-size:1.4rem;font-weight:700;color:#3b82f6;font-family:'Syne',sans-serif;">{currency(user.get('lump_sum_available', 0))}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Edit Profile"):
            with st.form("edit_profile"):
                new_income = st.number_input("Monthly Income (₹)", value=float(user.get("monthly_income", 0)), step=1000.0)
                new_expenses = st.number_input("Monthly Expenses (₹)", value=float(user.get("monthly_expenses", 0)), step=1000.0)
                new_lump = st.number_input("Lump Sum Available (₹)", value=float(user.get("lump_sum_available", 0)), step=1000.0)
                if st.form_submit_button("Save Changes", use_container_width=True):
                    result = api.update_profile(new_income, new_expenses, new_lump)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("Profile updated!")
                        st.rerun()

    with col_loans:
        st.markdown("<h3 style=\"font-family:'Syne',sans-serif;font-size:1.1rem;color:#f1f5f9;\">Active Loans</h3>", unsafe_allow_html=True)
        with st.expander("+ Add Loan", expanded=False):
            with st.form("add_loan"):
                fc1, fc2 = st.columns(2)
                with fc1:
                    lender = st.text_input("Lender Name", placeholder="HDFC Bank")
                    outstanding = st.number_input("Outstanding Amount (₹)", min_value=0.0, step=1000.0)
                    emi_val = st.number_input("Monthly EMI (₹)", min_value=0.0, step=500.0)
                with fc2:
                    loan_type = st.selectbox("Loan Type", ["Personal Loan","Home Loan","Car Loan","Credit Card","Education Loan","Business Loan","Other"])
                    interest = st.number_input("Interest Rate (%)", min_value=0.0, max_value=60.0, step=0.5)
                    overdue = st.number_input("Overdue Months", min_value=0, step=1)
                if st.form_submit_button("Add Loan", use_container_width=True):
                    if not lender or outstanding <= 0:
                        st.error("Lender name and outstanding amount are required.")
                    else:
                        result = api.add_loan(lender, loan_type, outstanding, interest, emi_val, int(overdue))
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.success(f"Loan from {lender} added!")
                            st.rerun()

        if not loans:
            st.markdown('<div class="fin-card" style="text-align:center;padding:3rem;"><div style="font-size:2rem;">🏦</div><div style="color:#94a3b8;">No loans yet. Click \'+ Add Loan\' above.</div></div>', unsafe_allow_html=True)
        else:
            priority_color = {"High":"#ef4444","Medium":"#f59e0b","Low":"#10b981"}
            for loan in loans:
                if not isinstance(loan, dict):
                    continue
                p = loan.get("priority", "Low")
                col = priority_color.get(p, "#10b981")
                lc1,lc2,lc3,lc4,lc5,lc6,_,lc8 = st.columns([2,1.5,1,1.2,1,1,1,0.8])
                with lc1:
                    st.markdown(f"<div style='font-weight:600;font-size:0.9rem;padding-top:0.5rem;'>{loan['lender_name']}</div><div style='font-size:0.75rem;color:#94a3b8;'>{loan['loan_type']}</div>", unsafe_allow_html=True)
                with lc2:
                    st.markdown(f"<div style='font-size:0.85rem;padding-top:0.5rem;'>₹{loan['outstanding_amount']:,.0f}</div>", unsafe_allow_html=True)
                with lc3:
                    st.markdown(f"<div style='color:#94a3b8;font-size:0.85rem;padding-top:0.5rem;'>{loan['interest_rate']}%</div>", unsafe_allow_html=True)
                with lc4:
                    st.markdown(f"<div style='font-size:0.85rem;padding-top:0.5rem;'>₹{loan['emi']:,.0f}</div>", unsafe_allow_html=True)
                with lc5:
                    overdue_months = int(loan.get("overdue_months", 0))
                    oc = "#ef4444" if overdue_months > 0 else "#94a3b8"
                    st.markdown(f"<div style='color:{oc};font-size:0.85rem;padding-top:0.5rem;'>{overdue_months}mo</div>", unsafe_allow_html=True)
                with lc6:
                    st.markdown(f"<span style='display:inline-block;padding:2px 8px;border-radius:20px;font-size:0.65rem;font-weight:700;text-transform:uppercase;background:{col}18;color:{col};border:1px solid {col}40;margin-top:0.4rem;'>{p}</span>", unsafe_allow_html=True)
                with lc8:
                    loan_id = loan.get("loan_id")
                    if loan_id is not None and st.button("🗑️", key=f"del_{loan_id}", help="Delete loan"):
                        result = api.delete_loan(loan_id)
                        if "error" not in result:
                            st.rerun()
                st.markdown("<hr style='border-color:rgba(255,255,255,0.05);margin:0.25rem 0;'>", unsafe_allow_html=True)
