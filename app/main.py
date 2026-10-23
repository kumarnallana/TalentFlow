import os
from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers.jobs_router import router as jobs_router

# 1. Create database tables automatically if they don't exist
Base.metadata.create_all(bind=engine)

# 2. Ensure the uploads folder exists
os.makedirs("uploads", exist_ok=True)

# 3. Initialize app and register the jobs router
app = FastAPI(title="TalentFlow API")
app.include_router(jobs_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "healthy", "service": "TalentFlow Engine"}
