import os
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "workspace", "automation.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    name = Column(String)
    created = Column(DateTime, default=datetime.utcnow)


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id"))
    tool = Column(String)
    execution_order = Column(Integer)


class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id"))
    frequency = Column(String)  # daily, weekly
    time = Column(String)
    status = Column(String, default="active")


class TaskQueue(Base):
    __tablename__ = "task_queue"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id"))
    status = Column(String, default="pending")  # pending, running, completed, failed
    added_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    alert_type = Column(String)
    message = Column(Text)
    severity = Column(String)
    read = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.utcnow)


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String, ForeignKey("workflows.id"))
    status = Column(String)
    duration = Column(String)
    completed_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_automation_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
