from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import db_ping
from app.deps import get_db
from app.models.company import Company
from app.schemas import CompanyCreate, CompanyOut, CompanyUpdate

app = FastAPI(title="Internship Tracker API")

TEMP_USER_ID = 1  # replace with real auth later

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db/ping")
def ping_db():
    ok = db_ping()
    return {"db": "ok" if ok else "down"}

@app.post("/companies", response_model=CompanyOut, status_code=201)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(
        user_id=TEMP_USER_ID,
        name=payload.name,
        website=str(payload.website) if payload.website else None,
        notes=payload.notes,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@app.get("/companies", response_model=list[CompanyOut])
def list_companies(db: Session = Depends(get_db)):
    stmt = (
        select(Company)
        .where(Company.user_id == TEMP_USER_ID)
        .order_by(Company.id.desc())
    )
    return list(db.scalars(stmt).all())

@app.get("/companies/{company_id}", response_model=CompanyOut)
def get_company(company_id: int, db: Session = Depends(get_db)):
    stmt = select(Company).where(
        Company.id == company_id,
        Company.user_id == TEMP_USER_ID,
    )
    company = db.scalars(stmt).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.patch("/companies/{company_id}", response_model=CompanyOut)
def update_company(company_id: int, payload: CompanyUpdate, db: Session = Depends(get_db)):
    stmt = select(Company).where(
        Company.id == company_id,
        Company.user_id == TEMP_USER_ID,
    )
    company = db.scalars(stmt).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    data = payload.model_dump(exclude_unset=True)

    if "name" in data:
        company.name = data["name"]
    if "website" in data:
        company.website = str(data["website"]) if data["website"] else None
    if "notes" in data:
        company.notes = data["notes"]

    db.commit()
    db.refresh(company)
    return company

@app.delete("/companies/{company_id}", status_code=204)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    stmt = select(Company).where(
        Company.id == company_id,
        Company.user_id == TEMP_USER_ID,
    )
    company = db.scalars(stmt).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(company)
    db.commit()
    return None