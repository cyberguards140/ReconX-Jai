import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workspace', 'jobs.db'))
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tool_id = Column(String)
    project_id = Column(String)
    target = Column(String, nullable=True)
    command = Column(String)
    status = Column(String, default="queued") # queued, running, completed, failed, cancelled
    pid = Column(Integer, nullable=True)
    started = Column(DateTime, nullable=True)
    finished = Column(DateTime, nullable=True)

class JobLog(Base):
    __tablename__ = "job_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_id = Column(String, ForeignKey("jobs.id"))
    output_type = Column(String) # stdout, stderr
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_job_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
