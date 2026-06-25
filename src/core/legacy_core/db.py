import os
import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "workspace", "projects.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True)
    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = Column(String, default="")
    project_type = Column(String, default="Custom")
    tags = Column(JSON, default=list)
    owner = Column(String, default="")
    status = Column(String, default="active")
    target_count = Column(Integer, default=0)
    finding_count = Column(Integer, default=0)
    archived = Column(Boolean, default=False)
    archived_date = Column(DateTime, nullable=True)


class Target(Base):
    __tablename__ = "targets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    type = Column(String)
    value = Column(String)
    added = Column(DateTime, default=datetime.utcnow)
    tag = Column(String, default="")


class Note(Base):
    __tablename__ = "notes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    title = Column(String)
    content = Column(String)
    created = Column(DateTime, default=datetime.utcnow)


class History(Base):
    __tablename__ = "history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
