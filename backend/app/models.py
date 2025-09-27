"""
models.py - SQLAlchemy ORM models for the transcription service.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, ForeignKey, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
from backend.app.db import Base

import uuid


class User(Base):
    """
    User of the transcription service.
    """
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    passwordHash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"


class License(Base):
    """
    License assigned to a user, with plan and features.
    """
    __tablename__ = "license"

    key = Column(String, primary_key=True)
    assignedToUserId = Column(String, ForeignKey("user.id"), nullable=True)
    plan = Column(String, nullable=False)
    features = Column(JSONB, nullable=False)
    validFrom = Column(DateTime, nullable=False)
    validUntil = Column(DateTime, nullable=False)
    isRevoked = Column(Boolean, default=False, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<License key={self.key} plan={self.plan} user={self.assignedToUserId}>"


class Job(Base):
    """
    Transcription job submitted by a user.
    """
    __tablename__ = "job"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ownerUserId = Column(String, ForeignKey("user.id"), nullable=False)
    status = Column(String, nullable=False)
    modelName = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    language = Column(String, nullable=True)
    audioDurationMs = Column(Integer, nullable=True)
    processingTimeMs = Column(Integer, nullable=True)
    resultJsonPath = Column(String, nullable=True)
    transcriptTxtPath = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = Column(DateTime, default=datetime.utcnow,
                       onupdate=datetime.utcnow, nullable=False)
    errorMessage = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<Job id={self.id} status={self.status} model={self.modelName}>"


class FileArtifact(Base):
    """
    File artifact associated with a job (e.g., uploaded audio, result files).
    """
    __tablename__ = "file_artifact"
    __table_args__ = (UniqueConstraint("jobId", "type", name="uix_job_type"),)

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    jobId = Column(String, ForeignKey("job.id"), nullable=False)
    type = Column(String, nullable=False)
    path = Column(String, nullable=False)
    sizeBytes = Column(Integer, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<FileArtifact id={self.id} jobId={self.jobId} type={self.type}>"
