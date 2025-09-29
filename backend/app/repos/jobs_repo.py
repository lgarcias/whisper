from typing import List, Optional

from app.models import Job
from sqlalchemy.orm import Session


def create_job(db: Session, **kwargs) -> Job:
    """Create and persist a new job."""
    job = Job(**kwargs)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job_by_id(db: Session, job_id: str) -> Optional[Job]:
    """Retrieve a job by ID."""
    return db.query(Job).filter(Job.id == job_id).first()


def list_jobs_by_user(db: Session, user_id: str, limit: int = 20, offset: int = 0) -> List[Job]:
    """List jobs for a given user."""
    return db.query(Job).filter(Job.owner_user_id == user_id).offset(offset).limit(limit).all()


def set_job_status(db: Session, job_id: str, status: str) -> Job:
    """Update the status of a job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise ValueError("Job not found")
    setattr(job, "status", status)
    db.commit()
    db.refresh(job)
    return job
