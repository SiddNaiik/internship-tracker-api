from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.companies import router as companies_router
from app.api.applications import router as applications_router

app = FastAPI(title="Internship Tracker API")

app.include_router(auth_router)
app.include_router(companies_router)
app.include_router(applications_router)

@app.get("/health")
def health():
    return {"status": "ok"}
