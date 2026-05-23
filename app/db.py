import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://app:app@localhost:5432/internship_tracker")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def db_ping() -> bool:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True