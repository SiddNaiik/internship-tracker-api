from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import db_ping
from app.deps import get_db
from app.models.company import Company
from app.models.application import Application
from app.schemas import CompanyCreate, CompanyOut, CompanyUpdate, ApplicationCreate, ApplicationOut, ApplicationUpdate

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

@app.post("/applications", response_model=ApplicationOut, status_code=201)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    # Ensure the company belongs to this user (prevents attaching to someone else’s company)
    company_stmt = select(Company).where(
        Company.id == payload.company_id,
        Company.user_id == TEMP_USER_ID,
    )
    company = db.scalars(company_stmt).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    app_row = Application(
        user_id=TEMP_USER_ID,
        company_id=payload.company_id,
        role_title=payload.role_title,
        job_url=str(payload.job_url) if payload.job_url else None,
        location=payload.location,
        status=payload.status,
    )
    db.add(app_row)
    db.commit()
    db.refresh(app_row)
    return app_row

@app.get("/applications", response_model=list[ApplicationOut])
def list_applications(db: Session = Depends(get_db)):
    stmt = (
        select(Application)
        .where(Application.user_id == TEMP_USER_ID)
        .order_by(Application.id.desc())
    )
    return list(db.scalars(stmt).all())

@app.get("/applications/{application_id}", response_model=ApplicationOut)
def get_application(application_id: int, db: Session = Depends(get_db)):
    stmt = select(Application).where(
        Application.id == application_id,
        Application.user_id == TEMP_USER_ID,
    )
    app_row = db.scalars(stmt).first()
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_row

@app.patch("/applications/{application_id}", response_model=ApplicationOut)
def update_application(application_id: int, payload: ApplicationUpdate, db: Session = Depends(get_db)):
    stmt = select(Application).where(
        Application.id == application_id,
        Application.user_id == TEMP_USER_ID,
    )
    app_row = db.scalars(stmt).first()
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")

    data = payload.model_dump(exclude_unset=True)

    # If company_id is being changed, ensure the new company belongs to user
    if "company_id" in data:
        company_stmt = select(Company).where(
            Company.id == data["company_id"],
            Company.user_id == TEMP_USER_ID,
        )
        company = db.scalars(company_stmt).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        app_row.company_id = data["company_id"]

    if "role_title" in data:
        app_row.role_title = data["role_title"]
    if "job_url" in data:
        app_row.job_url = str(data["job_url"]) if data["job_url"] else None
    if "location" in data:
        app_row.location = data["location"]
    if "status" in data:
        app_row.status = data["status"]

    db.commit()
    db.refresh(app_row)
    return app_row

@app.delete("/applications/{application_id}", status_code=204)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    stmt = select(Application).where(
        Application.id == application_id,
        Application.user_id == TEMP_USER_ID,
    )
    app_row = db.scalars(stmt).first()
    if not app_row:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(app_row)
    db.commit()
    return None