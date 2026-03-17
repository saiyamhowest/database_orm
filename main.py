from fastapi import FastAPI
from database import start_db


app = FastAPI()


@app.on_event("startup")
def on_startup():
    start_db()

    
@app.get("/")
def root():
    return {"message": "Bird API running"}