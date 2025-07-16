from fastapi import FastAPI
from app.database import engine
from app import models  # Ensure all models are imported for migrations

app = FastAPI()

# Include routers
# from app.routes.auth import router as auth_router
# app.include_router(auth_router)

# Optional startup/shutdown events
@app.on_event("startup")
def startup():
    # Anything you want here, like DB warm-up
    pass

@app.get("/")
def root():
    return {"message": "Status API is live"}
