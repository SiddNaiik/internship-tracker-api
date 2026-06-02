import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.models.base import Base
import app.models

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg://app:app@localhost:5432/internship_tracker")

def get_engine(url: str = DATABASE_URL):
    return create_engine(url, pool_pre_ping=True)

from sqlalchemy.engine import make_url

u = make_url(DATABASE_URL)
print(
    f"DB URL -> {u.drivername}://{u.username}:***@{u.host}:{u.port}/{u.database}"
)

engine = get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def db_ping() -> bool:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True