from pathlib import Path
from pypdf import PdfReader
from app.core.database import SessionLocal
from app.models.job import JobModel


def read_file_conetent(file_path: str) -> str:

    if not Path(file_path).is_file:
        raise FileNotFoundError(f"{file} is not found!!")

    if file_path.endswith(".pdf"):
        file_reader = PdfReader(file_path)
        ext_pages = file_reader.pages
        all_text = ""

        for page in ext_pages:
            text = page.extract_text()

            if text:
                all_text += text + "\n"

            return all_text

    elif file_path.endswith(".txt"):
        with open(file_path, "r", errors="ignore") as file:
            return file.read()

    raise ValueError(f"{file_path} type is not supported (eg: .pdf, .txt)")


def process_resume_job(job_id: int):
    db = SessionLocal()

    try:
        job = db.query(JobModel).filter(JobModel.id == job_id).first()
        if not job:
            return

        db.status = "Processing..."
        db.commit()

        matched_skills = []
    # extract text from the resume
        text = read_file_conetent(job.file_path)
        if job.target_skills:
            for skill in job.target_skills:
                if skill.lower() == text.lower():
                    matched_skills.append(skill)

        job_extracted_data = {
            "matched_skills": matched_skills,
            "match_count": len(matched_skills),
            "text_length": len(text)
        }

        job.status = "Completed..."
        db.commit()

    except Exception as e:
        job = db.query(JobModel).filter(JobModel.id == job_id).first()
        if job:
            job.status = "failed!"
            job.error_message = str(e)
            db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    process_resume_job()
