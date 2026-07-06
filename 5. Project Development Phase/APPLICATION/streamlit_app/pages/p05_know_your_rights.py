import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from components import rights_card

@st.cache_data(ttl=3600)
def get_rights_data():
    return [
        ("🚫","No Harassment","Lenders cannot use abusive language, threaten, or intimidate borrowers during debt recovery. All communication must be respectful.","#ef4444"),
        ("📄","Right to Information","You have the right to receive complete loan statements, outstanding details, and all charges in writing upon request.","#3b82f6"),
        ("🤝","Settlement Negotiation","Borrowers can negotiate settlement amounts directly with lenders. There is no legal obligation to pay more than mutually agreed.","#10b981"),
        ("📊","Credit Bureau Reporting","You have the right to know how your account is reported. Request 'Settled' status post-settlement.","#f59e0b"),
        ("✉️","Written Communication","Demand all settlement offers in writing before payment. Verbal agreements are not legally binding.","#8b5cf6"),
        ("⚖️","RBI Fair Practices","Under RBI Fair Practices Code, banks must follow ethical collection practices and cannot intimidate borrowers.","#06b6d4"),
        ("🔒","Privacy Rights","Your personal financial information cannot be shared with unauthorized third parties. DPDP Act 2023 protects your data.","#ec4899"),
        ("🛡️","Dispute Rights","You can dispute incorrect charges or unauthorized fees. Banks must respond within 30 days.","#14b8a6"),
    ]

def show():
    st.markdown('<div class="page-header"><h1>Know Your Rights</h1><p>Understanding your legal protections as a borrower in India</p></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="fin-card" style="border-left:4px solid #3b82f6;margin-bottom:2rem;">
      <div style="font-size:1rem;font-weight:600;margin-bottom:0.5rem;">🏛️ Your Borrower Rights Are Protected by Law</div>
      <p style="color:#94a3b8;font-size:0.875rem;line-height:1.7;margin:0;">
        The Reserve Bank of India (RBI) and Indian consumer protection laws provide strong safeguards for borrowers.
        Lenders must follow fair practices during recovery. Understanding your rights empowers you to negotiate confidently.
      </p>
    </div>""", unsafe_allow_html=True)

    rights = get_rights_data()
    col1, col2 = st.columns(2)
    for i, (icon, title, desc, color) in enumerate(rights):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(rights_card(icon, title, desc, color), unsafe_allow_html=True)

    st.markdown("""
    <div class="fin-card" style="border-left:4px solid #ef4444;margin-top:1rem;">
      <div style="font-size:1rem;font-weight:700;margin-bottom:1rem;">⚡ What To Do If You Face Harassment</div>""", unsafe_allow_html=True)

    a1, a2, a3, a4 = st.columns(4)
    for col, icon, title, desc in [
        (a1,"📝","Document Everything","Record all harassing calls, messages, and visits with dates and times."),
        (a2,"🏦","File Bank Complaint","Submit written complaint to the bank's Grievance Redressal Officer."),
        (a3,"🏛️","RBI Ombudsman","File online complaint at cms.rbi.org.in — free, resolved in 30 days."),
        (a4,"👮","Police/Legal Aid","File FIR for criminal intimidation. Seek free legal aid from DLSA."),
    ]:
        with col:
            st.markdown(f'<div class="tip-card" style="text-align:center;"><div style="font-size:1.8rem;margin-bottom:0.5rem;">{icon}</div><div style="font-weight:600;font-size:0.875rem;margin-bottom:0.25rem;">{title}</div><div style="font-size:0.78rem;color:#94a3b8;line-height:1.5;">{desc}</div></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    if "rights_acknowledged" not in st.session_state:
        st.session_state["rights_acknowledged"] = False

    if not st.session_state["rights_acknowledged"]:
        if st.button("✅  I Understand My Rights — Proceed Confidently", use_container_width=True):
            st.session_state["rights_acknowledged"] = True
            st.rerun()
    else:
        st.success("Rights acknowledged. You are empowered to negotiate with confidence!")
