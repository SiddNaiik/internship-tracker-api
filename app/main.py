from fastapi import FastAPI
from app.db import db_ping

app = FastAPI(title = "Internship Tracker API")

@app.get("/health")
def health():
    return {"status" : "ok"}

@app.get("/db/ping")
def ping_db():
    ok = db_ping()
    return {"db" if ok else "down"}