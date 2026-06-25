import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "exposure.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Exposure(Base):
    __tablename__ = "exposures"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    asset_id = Column(String)
    exposure_type = Column(String)  # external_service, missing_patch
    severity = Column(String)
    status = Column(String, default="Open")  # Open, Assigned, Remediated, Closed
    created_at = Column(DateTime, default=datetime.utcnow)


class RiskScore(Base):
    __tablename__ = "risk_scores"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exposure_id = Column(String, ForeignKey("exposures.id"))
    score = Column(Float, default=0.0)  # 0-100
    calculated_at = Column(DateTime, default=datetime.utcnow)


class BusinessCriticality(Base):
    __tablename__ = "business_criticality"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, unique=True)
    criticality = Column(String)  # Low, Medium, High, Critical
    assigned_at = Column(DateTime, default=datetime.utcnow)


class Ownership(Base):
    __tablename__ = "ownership"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, unique=True)
    owner = Column(String)  # Team or Business Unit
    assigned_at = Column(DateTime, default=datetime.utcnow)


class SLAPolicy(Base):
    __tablename__ = "sla_policies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    severity = Column(String, unique=True)
    deadline_days = Column(Integer)


class RemediationAction(Base):
    __tablename__ = "remediation_actions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    exposure_id = Column(String, ForeignKey("exposures.id"))
    action_plan = Column(Text)
    status = Column(String, default="Pending")  # Pending, In Progress, Verified
    updated_at = Column(DateTime, default=datetime.utcnow)


class SecurityPosture(Base):
    __tablename__ = "posture_scores"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    score = Column(Float)  # 0-100
    grade = Column(String)  # A, B, C, D, F
    calculated_at = Column(DateTime, default=datetime.utcnow)


class RiskReduction(Base):
    __tablename__ = "risk_reduction"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    reduction_percentage = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_exposure_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
