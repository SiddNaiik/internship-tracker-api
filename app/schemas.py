from pydantic import BaseModel, Field, HttpUrl
from app.enums import ApplicationStatus

class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    website: HttpUrl | None = None
    notes: str | None = Field(default=None, max_length=2000)


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    website: HttpUrl | None = None
    notes: str | None = Field(default=None, max_length=2000)


class CompanyOut(BaseModel):
    id: int
    name: str
    website: str | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


class ApplicationCreate(BaseModel):
    company_id: int
    role_title: str = Field(min_length=1, max_length=200)
    job_url: HttpUrl | None = None
    location: str | None = Field(default=None, max_length=200)
    status: ApplicationStatus = ApplicationStatus.applied


class ApplicationUpdate(BaseModel):
    company_id: int | None = None
    role_title: str | None = Field(default=None, min_length=1, max_length=200)
    job_url: HttpUrl | None = None
    location: str | None = Field(default=None, max_length=200)
    status: ApplicationStatus | None = None


class ApplicationOut(BaseModel):
    id: int
    company_id: int
    role_title: str
    job_url: str | None = None
    location: str | None = None
    status: ApplicationStatus

    class Config:
        from_attributes = True

class RegisterIn(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    password: str = Field(min_length=8, max_length=72)

class LoginIn(BaseModel):
    email: str
    password: str = Field(min_length=8, max_length=72)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"