import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'workspace', 'findings.db'))
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Finding(Base):
    __tablename__ = "findings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    category = Column(String, nullable=True)
    severity = Column(String) # critical, high, medium, low, info
    asset_id = Column(String) # linked to assets.db
    project_id = Column(String)
    tool = Column(String)
    cve = Column(String, nullable=True)
    evidence_path = Column(String, nullable=True)
    status = Column(String, default="open") # open, investigating, confirmed, false positive, resolved, suppressed
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class CVE(Base):
    __tablename__ = "cves"
    id = Column(String, primary_key=True) # e.g. CVE-2025-XXXX
    cvss_base = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    references = Column(Text, nullable=True)

class RiskScore(Base):
    __tablename__ = "risk_scores"
    finding_id = Column(String, ForeignKey("findings.id"), primary_key=True)
    calculated_score = Column(Float, default=0.0)

class FindingHistory(Base):
    __tablename__ = "finding_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    finding_id = Column(String, ForeignKey("findings.id"))
    event_description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_finding_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
