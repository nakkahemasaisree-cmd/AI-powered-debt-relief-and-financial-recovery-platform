import os
import streamlit as st
import requests
from typing import Dict, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def _headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}

def _handle(response, endpoint):
    if response.status_code == 401:
        st.session_state.clear()
        st.session_state["auth_error"] = "Session expired. Please sign in again."
        st.rerun()
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", f"Error {response.status_code}")
        except:
            detail = f"HTTP {response.status_code}"
        return {"error": detail}
    try:
        return response.json()
    except:
        return {"error": "Invalid response"}

def register(name, email, password, monthly_income, monthly_expenses, lump_sum):
    try:
        r = requests.post(f"{API_BASE_URL}/register", json={
            "name": name, "email": email, "password": password,
            "monthly_income": monthly_income, "monthly_expenses": monthly_expenses,
            "lump_sum_available": lump_sum,
        }, timeout=10)
        return _handle(r, "/register") or {}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend. Is the FastAPI server running on port 8000?"}
    except Exception as e:
        return {"error": str(e)}

def login(email, password):
    try:
        r = requests.post(f"{API_BASE_URL}/login", data={"username": email, "password": password}, timeout=10)
        return _handle(r, "/login") or {}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend. Is the FastAPI server running on port 8000?"}
    except Exception as e:
        return {"error": str(e)}

def update_profile(monthly_income, monthly_expenses, lump_sum):
    try:
        r = requests.put(f"{API_BASE_URL}/update-profile", json={
            "monthly_income": monthly_income, "monthly_expenses": monthly_expenses,
            "lump_sum_available": lump_sum,
        }, headers=_headers(), timeout=10)
        return _handle(r, "/update-profile") or {}
    except Exception as e:
        return {"error": str(e)}

def add_loan(lender_name, loan_type, outstanding_amount, interest_rate, emi, overdue_months):
    try:
        r = requests.post(f"{API_BASE_URL}/add-loan", json={
            "lender_name": lender_name, "loan_type": loan_type,
            "outstanding_amount": outstanding_amount, "interest_rate": interest_rate,
            "emi": emi, "overdue_months": overdue_months,
        }, headers=_headers(), timeout=10)
        return _handle(r, "/add-loan") or {}
    except Exception as e:
        return {"error": str(e)}

def get_loans():
    try:
        r = requests.get(f"{API_BASE_URL}/loans", headers=_headers(), timeout=10)
        return _handle(r, "/loans") or []
    except Exception as e:
        return {"error": str(e)}

def delete_loan(loan_id):
    try:
        r = requests.delete(f"{API_BASE_URL}/delete-loan/{loan_id}", headers=_headers(), timeout=10)
        return _handle(r, f"/delete-loan/{loan_id}") or {}
    except Exception as e:
        return {"error": str(e)}

def get_dashboard_data():
    try:
        r = requests.get(f"{API_BASE_URL}/dashboard-data", headers=_headers(), timeout=10)
        return _handle(r, "/dashboard-data") or {}
    except Exception as e:
        return {"error": str(e)}

def get_financial_health():
    try:
        r = requests.get(f"{API_BASE_URL}/financial-health", headers=_headers(), timeout=10)
        return _handle(r, "/financial-health") or {}
    except Exception as e:
        return {"error": str(e)}

def get_settlement_predictor():
    try:
        r = requests.get(f"{API_BASE_URL}/settlement-predictor", headers=_headers(), timeout=10)
        return _handle(r, "/settlement-predictor") or {}
    except Exception as e:
        return {"error": str(e)}

def get_ai_strategy():
    try:
        r = requests.get(f"{API_BASE_URL}/ai-negotiation-strategy", headers=_headers(), timeout=30)
        return _handle(r, "/ai-negotiation-strategy") or {}
    except Exception as e:
        return {"error": str(e)}

def generate_email(loan_id):
    try:
        r = requests.get(f"{API_BASE_URL}/generate-negotiation-email/{loan_id}", headers=_headers(), timeout=30)
        return _handle(r, f"/generate-negotiation-email/{loan_id}") or {}
    except Exception as e:
        return {"error": str(e)}

def get_ai_history():
    try:
        r = requests.get(f"{API_BASE_URL}/ai-history", headers=_headers(), timeout=10)
        return _handle(r, "/ai-history") or {}
    except Exception as e:
        return {"error": str(e)}

def get_debt_timeline(extra_payment: float = 0.0):
    try:
        r = requests.get(f"{API_BASE_URL}/debt-timeline", params={"extra_payment": extra_payment}, headers=_headers(), timeout=10)
        return _handle(r, "/debt-timeline") or {}
    except Exception as e:
        return {"error": str(e)}
