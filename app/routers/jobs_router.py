import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.job import JobModel
from app.schemas.jobs_schemas import JobAcceptedResponse, JobDetailResponse, Pagination
from app.services.data_extractor import get_data_from_db, process_resume_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=list[JobDetailResponse])
def list_jobs(pagination: Pagination = Depends(), db: Session = Depends(get_db)):
    return get_data_from_db(db, pagination)


@router.get("/{job_id}", response_model=JobDetailResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(JobModel, job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job


@router.post("/", status_code=202, response_model=JobAcceptedResponse)
def upload_resume(
    bg: BackgroundTasks,
    file: UploadFile,
    skills: str = Form(""),
    db: Session = Depends(get_db),
):
    if not file.filename or not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(400, "Only .pdf and .txt allowed")

    Path("uploads").mkdir(parents=True, exist_ok=True)
    job_id = str(uuid4())
    safe_filename = Path(file.filename).name
    file_path = f"uploads/{job_id}_{safe_filename}"

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    job = JobModel(
        id=job_id,
        filename=file.filename,
        file_path=file_path,
        target_skills=[s.strip() for s in skills.split(",") if s.strip()],
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    bg.add_task(process_resume_job, job.id)
    return job
