from sqlalchemy import select
from pathlib import Path
from pypdf import PdfReader
from app.core.database import SessionLocal
from app.models.job import JobModel
from app.schemas.jobs_schemas import Pagination
from sqlalchemy.orm import Session


def read_file_content(file_path: str) -> str:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"{file_path} is not found!!")

    lower_path = file_path.lower()
    if lower_path.endswith(".pdf"):
        file_reader = PdfReader(file_path)
        all_text = ""
        for page in file_reader.pages:
            text = page.extract_text()
            if text:
                all_text += text + "\n"
        return all_text

    elif lower_path.endswith(".txt"):
        with open(file_path, "r", errors="ignore") as file:
            return file.read()

    raise ValueError(f"{file_path} type is not supported (eg: .pdf, .txt)")


def process_resume_job(job_id: str):
    db = SessionLocal()

    try:
        job = db.query(JobModel).filter(JobModel.id == job_id).first()
        if not job:
            return

        job.status = "processing"
        db.commit()

        matched_skills = []
        text = read_file_content(job.file_path)
        if job.target_skills:
            for skill in job.target_skills:
                if skill.lower() in text.lower():
                    matched_skills.append(skill)

        job_extracted_data = {
            "matched_skills": matched_skills,
            "match_count": len(matched_skills),
            "text_length": len(text),
        }

        job.extracted_data = job_extracted_data
        job.status = "completed"
        db.commit()

    except Exception as e:
        db.rollback()
        job = db.query(JobModel).filter(JobModel.id == job_id).first()
        if job:
            job.status = "failed"
            job.error_message = str(e)
            db.commit()

    finally:
        db.close()


def get_all_data(db: Session, pagination: Pagination) -> list[JobModel]:
    statement = (
        select(JobModel)
        .order_by(JobModel.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
    )
    result = db.scalars(statement)
    return list(result.all())


def get_data_from_db(db: Session, pagination: Pagination) -> list[JobModel]:
    return get_all_data(db, pagination)
