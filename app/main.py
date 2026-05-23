from fastapi import FastAPI

app = FastAPI(title = "Internship Tracker API")

@app.get("/health")
def health():
    return {"status" : "ok"}