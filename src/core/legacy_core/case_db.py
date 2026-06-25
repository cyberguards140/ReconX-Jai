import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "workspace", "cases.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Case(Base):
    __tablename__ = "cases"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, unique=True)
    case_type = Column(String)  # Threat, Exposure, Asset, Cloud
    status = Column(
        String, default="Open"
    )  # Open, Assigned, In Progress, Pending Review, Resolved, Closed
    created_at = Column(DateTime, default=datetime.utcnow)


class Investigation(Base):
    __tablename__ = "investigations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    investigation_name = Column(String)
    owner = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class EvidenceChain(Base):
    __tablename__ = "evidence_chain"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    evidence_type = Column(String)
    file_hash = Column(String)  # SHA256
    source = Column(String)
    creator = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Artifact(Base):
    __tablename__ = "artifacts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    artifact_name = Column(String)
    artifact_type = Column(String)  # export, report
    file_path = Column(String)
    generated_at = Column(DateTime, default=datetime.utcnow)


class CaseAssignment(Base):
    __tablename__ = "case_assignments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    assignee = Column(String)
    assignment_type = Column(String)  # User, Team
    assigned_at = Column(DateTime, default=datetime.utcnow)


class CaseReview(Base):
    __tablename__ = "case_reviews"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    reviewer = Column(String)
    status = Column(String, default="Pending")  # Pending, Approved, Rejected, Needs Revision
    reviewed_at = Column(DateTime, nullable=True)


class CaseTimeline(Base):
    __tablename__ = "case_timeline"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, ForeignKey("cases.id"))
    event_description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_case_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
