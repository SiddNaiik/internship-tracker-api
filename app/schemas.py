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