import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import api_client as api
from components import stat_card, stress_badge, progress_bar, tip_card, currency
from typing import Any, Dict

def show():
    st.markdown('<div class="page-header"><h1>Financial Health</h1><p>Detailed analysis of your debt stress and repayment capacity</p></div>', unsafe_allow_html=True)

    with st.spinner("Analyzing..."):
        data: Dict[str, Any] = api.get_financial_health() or {}

    if not isinstance(data, dict) or "error" in data:
        st.error(f"Failed to load: {data.get('error', 'Unknown error') if isinstance(data, dict) else 'Invalid response'}")
        return

    stress = data.get("stress_level", "Low")
    stress_color = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}[stress]
    stress_desc = {
        "Low": "Your debt load is manageable. Keep maintaining your current payment discipline.",
        "Medium": "Your EMI burden is moderate. Consider restructuring or paying extra toward high-interest loans.",
        "High": "Your debt stress is high. Immediate action recommended — contact lenders for restructuring or settlement.",
    }[stress]

    st.markdown(f"""
    <div class="fin-card" style="display:flex;justify-content:space-between;align-items:center;border-left:4px solid {stress_color};">
      <div>
        <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:0.25rem;">Overall Financial Stress</div>
        <div style="color:#94a3b8;font-size:0.875rem;max-width:600px;">{stress_desc}</div>
      </div>
      <div>{stress_badge(stress)}</div>
    </div>
    """, unsafe_allow_html=True)

    user_data: Dict[str, Any] = data.get("user", {}) if isinstance(data.get("user", {}), dict) else {}
    surplus = data.get("surplus", 0)
    surplus_color = "#ef4444" if surplus < 0 else "#10b981"

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(stat_card("Monthly Income", currency(user_data.get("monthly_income", 0))), unsafe_allow_html=True)
    with m2: st.markdown(stat_card("Monthly Expenses", currency(user_data.get("monthly_expenses", 0))), unsafe_allow_html=True)
    with m3: st.markdown(stat_card("Monthly Surplus", currency(surplus), color=surplus_color), unsafe_allow_html=True)
    with m4: st.markdown(stat_card("Lump Sum Available", currency(user_data.get("lump_sum_available", 0))), unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    emi_ratio = data.get("emi_ratio_percent", 0)
    dti_ratio = data.get("debt_to_income_percent", 0)

    pr1, pr2 = st.columns(2)
    with pr1:
        emi_caption = "Critical" if emi_ratio > 50 else ("Warning" if emi_ratio > 30 else "Healthy range")
        st.markdown(f'<div class="fin-card"><div style="font-family:\'Syne\',sans-serif;font-weight:700;margin-bottom:1rem;">EMI-to-Income Ratio</div>{progress_bar(emi_ratio, caption=f"Ideal: Below 30% | Yours: {emi_ratio:.1f}% — {emi_caption}")}</div>', unsafe_allow_html=True)
    with pr2:
        dti_caption = "Critical" if dti_ratio > 80 else ("Moderate" if dti_ratio > 40 else "Healthy range")
        st.markdown(f'<div class="fin-card"><div style="font-family:\'Syne\',sans-serif;font-weight:700;margin-bottom:1rem;">Debt-to-Income Ratio</div>{progress_bar(min(dti_ratio, 100), caption=f"Ideal: Below 40% | Yours: {dti_ratio:.1f}% — {dti_caption}")}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div style=\"font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;margin-bottom:1rem;\">💡 Improvement Tips</div>", unsafe_allow_html=True)

    tips = [
        ("✂️","Reduce discretionary spending to increase monthly surplus and accelerate debt payoff."),
        ("🏦","Contact lenders proactively for EMI restructuring — many banks offer relief programs."),
        ("🎯","Use available lump sum for the highest-interest loan first to minimize total interest paid."),
        ("📊","Track all expenses monthly to identify hidden savings opportunities and free up cash."),
    ]
    t1, t2, t3, t4 = st.columns(4)
    for col, (icon, text) in zip([t1, t2, t3, t4], tips):
        with col:
            st.markdown(tip_card(icon, text), unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    with st.expander("📅 Debt Repayment Timeline Simulator"):
        extra = st.slider("Extra monthly payment (₹)", 0, 50000, 0, 500)
        if st.button("Simulate Timeline"):
            with st.spinner("Simulating..."):
                tl = api.get_debt_timeline(extra_payment=float(extra))
            if "error" in tl:
                st.error(tl["error"])
            else:
                months_free = tl.get("months_to_debt_free")
                remaining = tl.get("final_remaining_balance", 0)
                preview = tl.get("timeline_preview", [])
                if isinstance(months_free, int):
                    st.success(f"Debt-free in approximately **{months_free} months** ({months_free//12}y {months_free%12}m)")
                else:
                    st.warning(f"Remaining balance after 240 months: {currency(remaining)}")
                if preview:
                    import pandas as pd
                    df = pd.DataFrame(preview)
                    df.columns = ["Month", "Total Remaining (₹)"]
                    st.line_chart(df.set_index("Month"))
