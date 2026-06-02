from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.current_user import get_current_user
from app.deps import get_db
from app.models.company import Company
from app.models.user import User
from app.schemas import CompanyCreate, CompanyOut, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("", response_model=CompanyOut, status_code=201)
def create_company(
    payload: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    company = Company(
        user_id=current_user.id,
        name=payload.name,
        website=str(payload.website) if payload.website else None,
        notes=payload.notes,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("", response_model=list[CompanyOut])
def list_companies(
    q: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Company).where(Company.user_id == current_user.id)

    if q:
        # simple case-insensitive search
        stmt = stmt.where(Company.name.ilike(f"%{q}%"))

    stmt = stmt.order_by(Company.id.desc()).limit(limit).offset(offset)
    return list(db.scalars(stmt).all())


@router.get("/{company_id}", response_model=CompanyOut)
def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Company).where(
        Company.id == company_id,
        Company.user_id == current_user.id,
    )
    company = db.scalars(stmt).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.patch("/{company_id}", response_model=CompanyOut)
def update_company(
    company_id: int,
    payload: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Company).where(
        Company.id == company_id,
        Company.user_id == current_user.id,
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


@router.delete("/{company_id}", status_code=204)
def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Company).where(
        Company.id == company_id,
        Company.user_id == current_user.id,
    )
    company = db.scalars(stmt).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    db.delete(company)
    db.commit()
    return None