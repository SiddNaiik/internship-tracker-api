from pydantic import BaseModel, Field, HttpUrl


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
    status: str = Field(default="applied", max_length=50)


class ApplicationUpdate(BaseModel):
    company_id: int | None = None
    role_title: str | None = Field(default=None, min_length=1, max_length=200)
    job_url: HttpUrl | None = None
    location: str | None = Field(default=None, max_length=200)
    status: str | None = Field(default=None, max_length=50)


class ApplicationOut(BaseModel):
    id: int
    company_id: int
    role_title: str
    job_url: str | None = None
    location: str | None = None
    status: str

    class Config:
        from_attributes = True