try:
    from fastapi import FastAPI  # type: ignore
    from fastapi.middleware.cors import CORSMiddleware  # type: ignore
except Exception as e:
    raise ImportError(
        "FastAPI or its components could not be imported. Install dependencies with: pip install fastapi[all] uvicorn\nOriginal error: "
        + str(e)
    )
from dotenv import load_dotenv

load_dotenv()

from app.database import engine, Base
from app.models import User, Loan, FinancialProfile, SettlementPrediction, AINegotiation, AIHistory
from app.routers import auth, profile, loans, dashboard, ai

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinRelief AI",
    description="AI-Powered Debt Relief & Financial Recovery Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(loans.router)
app.include_router(dashboard.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "FinRelief AI API is running", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
