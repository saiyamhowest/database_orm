from fastapi import FastAPI
from database import start_db
from routers import species
from routers import birds
from routers import birdspotting

app = FastAPI()

app.include_router(birds.router)

app.include_router(species.router)

app.include_router(birdspotting.router)

@app.on_event("startup")
def on_startup():
    start_db()

    
@app.get("/")
def root():
    return {"message": "Bird API running"}