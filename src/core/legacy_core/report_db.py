import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "reports.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Report(Base):
    __tablename__ = "reports"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    report_type = Column(String)  # executive, technical, vulnerability, cloud, campaign
    version = Column(Integer, default=1)
    file_path = Column(String)
    created = Column(DateTime, default=datetime.utcnow)


class ReportTemplate(Base):
    __tablename__ = "report_templates"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(String)
    name = Column(String)
    path = Column(String)


class EvidencePackage(Base):
    __tablename__ = "evidence_packages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    file_path = Column(String)
    size = Column(Integer)
    created = Column(DateTime, default=datetime.utcnow)


class ReportHistory(Base):
    __tablename__ = "report_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id = Column(String, ForeignKey("reports.id"))
    action = Column(String)  # generated, downloaded, exported
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_report_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
