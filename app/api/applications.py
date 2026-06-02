from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.current_user import get_current_user
from app.deps import get_db
from app.enums import ApplicationStatus
from app.models.application import Application
from app.models.company import Company
from app.models.user import User
from app.schemas import ApplicationCreate, ApplicationOut, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationOut, status_code=201)
def create_application(
    payload: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ensure company belongs to current user
    company = db.scalars(
        select(Company).where(
            Company.id == payload.company_id,
            Company.user_id == current_user.id,
        )
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    row = Application(
        user_id=current_user.id,
        company_id=payload.company_id,
        role_title=payload.role_title,
        job_url=str(payload.job_url) if payload.job_url else None,
        location=payload.location,
        status=payload.status,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.get("", response_model=list[ApplicationOut])
def list_applications(
    company_id: int | None = Query(default=None),
    status: ApplicationStatus | None = Query(default=None),  # optional filter (you can also type this as ApplicationStatus)
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(Application).where(Application.user_id == current_user.id)

    if company_id is not None:
        stmt = stmt.where(Application.company_id == company_id)
    if status is not None:
        stmt = stmt.where(Application.status == status)

    stmt = stmt.order_by(Application.id.desc()).limit(limit).offset(offset)
    return list(db.scalars(stmt).all())


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.scalars(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")
    return row


@router.patch("/{application_id}", response_model=ApplicationOut)
def update_application(
    application_id: int,
    payload: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.scalars(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    data = payload.model_dump(exclude_unset=True)

    if "company_id" in data:
        company = db.scalars(
            select(Company).where(
                Company.id == data["company_id"],
                Company.user_id == current_user.id,
            )
        ).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        row.company_id = data["company_id"]

    if "role_title" in data:
        row.role_title = data["role_title"]
    if "job_url" in data:
        row.job_url = str(data["job_url"]) if data["job_url"] else None
    if "location" in data:
        row.location = data["location"]
    if "status" in data:
        row.status = data["status"]

    db.commit()
    db.refresh(row)
    return row


@router.delete("/{application_id}", status_code=204)
def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.scalars(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id,
        )
    ).first()
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(row)
    db.commit()
    return None