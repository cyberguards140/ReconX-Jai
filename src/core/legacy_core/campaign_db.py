import os
import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "campaigns.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    campaign_type = Column(String)  # Red Team, External ASM
    status = Column(
        String, default="Draft"
    )  # Draft, Planning, Active, Reporting, Completed, Archived
    created_at = Column(DateTime, default=datetime.utcnow)


class Engagement(Base):
    __tablename__ = "engagements"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    engagement_name = Column(String)
    client = Column(String)
    status = Column(String, default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)


class AssessmentScope(Base):
    __tablename__ = "assessment_scopes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    target = Column(String)
    status = Column(String, default="In Scope")  # In Scope, Out of Scope, Pending Approval
    created_at = Column(DateTime, default=datetime.utcnow)


class CampaignTask(Base):
    __tablename__ = "campaign_tasks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    task_name = Column(String)
    task_type = Column(String)
    status = Column(String, default="Open")  # Open, Assigned, In Progress, Blocked, Completed
    assigned_to = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class CampaignMilestone(Base):
    __tablename__ = "campaign_milestones"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    milestone_name = Column(String)
    status = Column(String, default="Pending")  # Pending, Completed
    completed_at = Column(DateTime, nullable=True)


class CampaignTimeline(Base):
    __tablename__ = "campaign_timeline"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    event_description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Evidence(Base):
    __tablename__ = "evidence"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, ForeignKey("campaigns.id"))
    evidence_type = Column(String)  # screenshot, report, log
    file_path = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_campaign_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
