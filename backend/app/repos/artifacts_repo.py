from typing import List, Optional

from app.models import FileArtifact
from sqlalchemy.orm import Session


def add_artifact(db: Session, **kwargs) -> FileArtifact:
    """Create and persist a new file artifact."""
    artifact = FileArtifact(**kwargs)
    db.add(artifact)
    db.commit()
    db.refresh(artifact)
    return artifact


def list_artifacts_by_job(db: Session, job_id: str) -> List[FileArtifact]:
    """List all artifacts for a given job."""
    return db.query(FileArtifact).filter(FileArtifact.job_id == job_id).all()


def get_artifact_by_type(db: Session, job_id: str, type_: str) -> Optional[FileArtifact]:
    """Get a specific artifact by job and type."""
    return (
        db.query(FileArtifact)
        .filter(FileArtifact.job_id == job_id, FileArtifact.type == type_)
        .first()
    )
