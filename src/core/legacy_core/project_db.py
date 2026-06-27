import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.expanduser("~/ReconX/workspace"), "projects.db")
)
import os; os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    description = Column(String)
    client = Column(String)
    tags = Column(String)  # JSON list
    status = Column(String, default="Active")  # Active, Paused, Archived, Completed
    created = Column(DateTime, default=datetime.utcnow)


class Target(Base):
    __tablename__ = "targets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    target_type = Column(String)  # domain, ip, cidr, url, asn
    value = Column(String)
    scope = Column(String, default="in")  # in, out, excluded


class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    name = Column(String)
    status = Column(String, default="running")
    start_time = Column(DateTime, default=datetime.utcnow)


class ScanProfile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    tools = Column(Text)  # JSON list
    arguments = Column(Text)  # JSON dict
    created_by = Column(String, default="system")


class Note(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    title = Column(String)
    content = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)


class HistoryEvent(Base):
    __tablename__ = "history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, ForeignKey("projects.id"))
    event_type = Column(String)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)





def get_project_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
