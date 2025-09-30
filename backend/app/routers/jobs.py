from typing import List, Optional

from app.db import get_db
from app.repos.jobs_repo import create_job, get_job_by_id, list_jobs_by_user
from app.schemas import JobCreateIn, JobOut
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/transcriptions", tags=["transcriptions"])


@router.post("/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job_handler(
    job_in: JobCreateIn,
    response: Response,
    db: Session = Depends(get_db),
) -> JobOut:
    """Create a new transcription job."""
    try:
        job = create_job(db, **job_in.dict())
        if response is not None:
            response.headers["Location"] = f"/{job.id}"
        return job
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[JobOut])
def list_jobs_handler(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
) -> List[JobOut]:
    """List jobs for the current user, optionally filtered by status."""
    # TODO: Replace with actual user_id from auth/session
    user_id = "demo-user-id"
    jobs = list_jobs_by_user(db, user_id, limit=limit, offset=offset)
    if status:
        jobs = [job for job in jobs if str(job.status) == status]
    return [JobOut.model_validate(job) for job in jobs]


@router.get("/{job_id}", response_model=JobOut)
def get_job_detail_handler(
    job_id: str,
    db: Session = Depends(get_db),
) -> JobOut:
    """Get job details by ID."""
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobOut.model_validate(job)
