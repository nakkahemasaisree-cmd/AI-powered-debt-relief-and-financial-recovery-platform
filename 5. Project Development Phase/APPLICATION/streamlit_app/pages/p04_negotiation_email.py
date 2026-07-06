import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import api_client as api

def show():
    st.markdown('<div class="page-header"><h1>Negotiation Email Generator</h1><p>Generate professional, lender-specific settlement request letters using AI</p></div>', unsafe_allow_html=True)

    with st.spinner("Loading loans..."):
        loans_data = api.get_loans()

    loans = loans_data if isinstance(loans_data, list) else []
    if not loans:
        st.markdown('<div class="fin-card" style="text-align:center;padding:3rem;"><div style="font-size:2rem;">✉️</div><div style="color:#94a3b8;">No loans found. Add loans from the Dashboard first.</div></div>', unsafe_allow_html=True)
        return

    loan_options = {f"{l['lender_name']} — {l['loan_type']} (₹{l['outstanding_amount']:,.0f})": l["loan_id"] for l in loans}

    sel_col, btn_col = st.columns([3, 1])
    with sel_col:
        selected_label = st.selectbox("Select Loan Account", list(loan_options.keys()))
    with btn_col:
        st.markdown("<div style='height:1.7rem;'></div>", unsafe_allow_html=True)
        generate = st.button("Generate Letter", use_container_width=True)

    if generate:
        selected_loan_id = loan_options[selected_label]
        with st.spinner("Generating negotiation letter via AI..."):
            result = api.generate_email(selected_loan_id)
        if "error" in result:
            st.error(result["error"])
        else:
            st.session_state["generated_letter"] = result.get("letter", "")
            st.session_state["generated_letter_lender"] = result.get("lender_name", "")

    letter = st.session_state.get("generated_letter", "")
    lender = st.session_state.get("generated_letter_lender", "")

    if letter:
        hdr_col, dl_col = st.columns([4, 1])
        with hdr_col:
            st.markdown(f"<h3 style=\"font-family:'Syne',sans-serif;font-size:1.1rem;\">Negotiation Letter — {lender}</h3>", unsafe_allow_html=True)
        with dl_col:
            st.download_button("⬇ Download", data=letter, file_name=f"settlement_letter_{lender.replace(' ','_')}.txt", mime="text/plain", use_container_width=True)
        st.markdown(f'<div class="fin-card"><div class="letter-box">{letter}</div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="fin-card" style="border-left:3px solid #f59e0b;margin-top:1rem;">
          <div style="font-weight:600;color:#f59e0b;margin-bottom:0.5rem;">⚠️ Important Notes</div>
          <ul style="color:#94a3b8;font-size:0.875rem;line-height:1.8;margin:0;padding-left:1.25rem;">
            <li>Review the letter carefully — verify all amounts and personal details.</li>
            <li>Send via registered post or email with read receipt.</li>
            <li>Keep copies of all correspondence with the lender.</li>
            <li>Consult a certified financial advisor for personalized advice.</li>
          </ul>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="fin-card" style="text-align:center;padding:2.5rem;"><div style="font-size:2rem;margin-bottom:0.75rem;">✉️</div><div style="color:#94a3b8;">Select a loan and click <strong style="color:#3b82f6;">Generate Letter</strong> to create a personalized negotiation email.</div></div>', unsafe_allow_html=True)
