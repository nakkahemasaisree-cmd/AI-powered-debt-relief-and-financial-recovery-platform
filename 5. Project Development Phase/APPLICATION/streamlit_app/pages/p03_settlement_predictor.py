import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import api_client as api
from components import risk_badge, currency

def show():
    st.markdown('<div class="page-header"><h1>Settlement Predictor</h1><p>AI-powered settlement probability and negotiation strategy per loan</p></div>', unsafe_allow_html=True)

    with st.spinner("Calculating..."):
        data = api.get_settlement_predictor()

    if "error" in data:
        st.error(f"Failed to load: {data['error']}")
        return

    settlements = data.get("settlements", [])
    if not settlements:
        st.markdown('<div class="fin-card" style="text-align:center;padding:3rem;"><div style="font-size:2rem;">🎯</div><div style="color:#94a3b8;">No loans found. Add loans from Dashboard first.</div></div>', unsafe_allow_html=True)
        return

    for s in settlements:
        pct = s.get("suggested_settlement_percentage", 50)
        pct_color = "#10b981" if pct >= 65 else ("#f59e0b" if pct >= 55 else "#3b82f6")
        risk = s.get("risk_category", "Low")
        st.markdown(f"""
        <div class="fin-card" style="margin-bottom:1.5rem;">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1.5rem;">
            <div>
              <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:700;">{s['lender_name']}</div>
              <div style="color:#94a3b8;font-size:0.85rem;">Outstanding: {currency(s['outstanding_amount'])} · Rate: {s['interest_rate']}% · EMI: {currency(s['emi'])}</div>
            </div>
            <div>{risk_badge(risk)}</div>
          </div>
          <div style="display:flex;gap:2rem;align-items:center;">
            <div style="text-align:center;">
              <div style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:{pct_color};line-height:1;">{pct:.0f}%</div>
              <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;margin-top:4px;">Settlement Range</div>
            </div>
            <div style="width:1px;height:60px;background:rgba(255,255,255,0.08);"></div>
            <div>
              <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;">Predicted Amount</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;">{currency(s['predicted_amount'])}</div>
              <div style="font-size:0.8rem;color:#94a3b8;">of {currency(s['outstanding_amount'])}</div>
            </div>
            <div style="width:1px;height:60px;background:rgba(255,255,255,0.08);"></div>
            <div>
              <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;">Risk Score</div>
              <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:700;">{s['risk_score']}</div>
              <div style="font-size:0.8rem;color:#94a3b8;">out of 60</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style=\"font-family:'Syne',sans-serif;font-size:1.1rem;\">AI Negotiation Strategy</h3>", unsafe_allow_html=True)

    regen = st.button("🔄 Generate / Regenerate Strategy", use_container_width=False)
    if regen or "strategy_text" not in st.session_state:
        with st.spinner("Generating AI strategy..."):
            result = api.get_ai_strategy()
        if "error" in result:
            st.error(result["error"])
            return
        st.session_state["strategy_text"] = result.get("strategy", "")

    strategy = st.session_state.get("strategy_text", "")
    if strategy:
        st.markdown(f'<div class="fin-card"><pre style="font-family:\'DM Sans\',sans-serif;font-size:0.875rem;color:#cbd5e1;white-space:pre-wrap;word-wrap:break-word;line-height:1.7;margin:0;">{strategy}</pre></div>', unsafe_allow_html=True)
