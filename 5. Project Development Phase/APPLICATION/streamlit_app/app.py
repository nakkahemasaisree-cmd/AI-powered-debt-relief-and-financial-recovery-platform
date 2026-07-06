import os, sys
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
# Ensure the Streamlit app can import local modules from this folder.
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(page_title="FinRelief AI", page_icon="💳", layout="wide", initial_sidebar_state="collapsed")

css_path = Path(__file__).parent / "styles.css"
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

for key in ["token", "page", "user_name"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "token" else ("dashboard" if key == "page" else "")

def show_sidebar():
    pages = [
        ("dashboard","📊","Dashboard"),("financial_health","❤️","Financial Health"),
        ("settlement_predictor","🎯","Settlement Predictor"),("negotiation_email","✉️","Negotiation Email"),
        ("know_your_rights","⚖️","Know Your Rights"),("history","🕐","History"),
    ]
    with st.sidebar:
        st.markdown('<div style="padding:1.5rem 1rem 1rem;"><div style="font-family:\'Syne\',sans-serif;font-size:1.4rem;font-weight:800;color:#f1f5f9;padding-bottom:1rem;border-bottom:1px solid rgba(255,255,255,0.08);">Fin<span style="color:#3b82f6;">Relief</span> AI</div></div>', unsafe_allow_html=True)
        if st.session_state.get("user_name"):
            st.markdown(f'<div style="padding:0.5rem 1rem 1rem;border-bottom:1px solid rgba(255,255,255,0.08);"><div style="font-size:0.7rem;color:#475569;text-transform:uppercase;">Signed in as</div><div style="font-size:0.9rem;font-weight:600;color:#f1f5f9;">{st.session_state["user_name"]}</div></div>', unsafe_allow_html=True)
        for key, icon, label in pages:
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state["page"] = key
                st.rerun()
        st.markdown("<hr style='border-color:rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
        if st.button("🚪  Sign Out", key="signout", use_container_width=True):
            st.session_state.clear()
            st.session_state["page"] = "login"
            st.rerun()

def show_login():
    import api_client as api
    if st.session_state.get("auth_error"):
        st.error(st.session_state.pop("auth_error"))

    col_l, col_r = st.columns([1.1, 0.9])
    with col_l:
        st.markdown("""
        <div style="padding:3rem 2rem;min-height:80vh;display:flex;flex-direction:column;justify-content:center;">
          <div style="font-size:0.8rem;font-weight:600;color:#3b82f6;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:1rem;">AI-POWERED DEBT MANAGEMENT</div>
          <h1 style="font-family:'Syne',sans-serif;font-size:3rem;font-weight:800;color:#f1f5f9;line-height:1.1;margin-bottom:1rem;">
            Take Control of Your<br>
            <span style="background:linear-gradient(135deg,#2563eb,#10b981);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Financial Future</span>
          </h1>
          <p style="color:#94a3b8;font-size:1rem;line-height:1.6;max-width:420px;margin-bottom:2.5rem;">
            AI-powered debt management that helps you negotiate smarter, settle faster, and live debt-free sooner.
          </p>
        </div>""", unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        for col, big, small in [(s1,"40–75%","Settlement Range"),(s2,"AI","Powered Strategy"),(s3,"Free","To Get Started")]:
            with col:
                st.markdown(f'<div class="login-hero-stat"><div class="big">{big}</div><div class="small">{small}</div></div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div style="padding:2.5rem;background:var(--bg-card);border:1px solid var(--border-bright);border-radius:var(--radius-xl);margin:2rem 0;"><h2 style="font-family:\'Syne\',sans-serif;font-size:1.5rem;font-weight:700;color:#f1f5f9;margin-bottom:0.25rem;">Welcome back</h2><p style="color:#94a3b8;font-size:0.875rem;margin-bottom:1.5rem;">Sign in to your dashboard</p></div>', unsafe_allow_html=True)

        tab_si, tab_reg = st.tabs(["Sign In", "Register"])
        with tab_si:
            with st.form("signin"):
                email = st.text_input("Email Address", placeholder="you@example.com")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Sign In →", use_container_width=True):
                    if not email or not password:
                        st.error("Please fill in all fields.")
                    else:
                        with st.spinner("Signing in..."):
                            result = api.login(email, password)
                        if isinstance(result, dict) and "error" in result:
                            st.error(result["error"])
                        elif isinstance(result, dict):
                            st.session_state["token"] = result.get("access_token", "")
                            data = api.get_dashboard_data()
                            if isinstance(data, dict) and "user" in data:
                                st.session_state["user_name"] = data["user"].get("name", "")
                            st.session_state["page"] = "dashboard"
                            st.rerun()
                        else:
                            st.error("Unexpected login response")

        with tab_reg:
            with st.form("register"):
                name = st.text_input("Full Name")
                reg_email = st.text_input("Email Address", key="re")
                reg_pass = st.text_input("Password (min 6 chars)", type="password", key="rp")
                c1, c2 = st.columns(2)
                with c1:
                    income = st.number_input("Monthly Income (₹)", min_value=0.0, value=50000.0, step=1000.0)
                    lump = st.number_input("Lump Sum Available (₹)", min_value=0.0, step=1000.0)
                with c2:
                    expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=20000.0, step=1000.0)
                if st.form_submit_button("Create Account →", use_container_width=True):
                    if not all([name, reg_email, reg_pass]):
                        st.error("Please fill in all required fields.")
                    elif len(reg_pass) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        with st.spinner("Creating account..."):
                            result = api.register(name, reg_email, reg_pass, income, expenses, lump)
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            st.success("Account created! Please sign in.")

def main():
    if not st.session_state.get("token"):
        show_login()
        return

    show_sidebar()
    page = st.session_state.get("page", "dashboard")

    if page == "dashboard":
        from pages import p01_dashboard; p01_dashboard.show()
    elif page == "financial_health":
        from pages import p02_financial_health; p02_financial_health.show()
    elif page == "settlement_predictor":
        from pages import p03_settlement_predictor; p03_settlement_predictor.show()
    elif page == "negotiation_email":
        from pages import p04_negotiation_email; p04_negotiation_email.show()
    elif page == "know_your_rights":
        from pages import p05_know_your_rights; p05_know_your_rights.show()
    elif page == "history":
        from pages import p06_history; p06_history.show()

main()
