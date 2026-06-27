import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.expanduser("~/ReconX/workspace"), "analytics.db")
)
import os; os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class HistoricalSnapshot(Base):
    __tablename__ = "historical_snapshots"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    snapshot_date = Column(DateTime, default=datetime.utcnow)
    total_assets = Column(Integer, default=0)
    total_findings = Column(Integer, default=0)
    critical_findings = Column(Integer, default=0)
    risk_score = Column(Float, default=0.0)


class TrendData(Base):
    __tablename__ = "trend_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    trend_category = Column(String)  # Asset Growth, Risk Growth
    delta_value = Column(Float)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class ExecutiveMetric(Base):
    __tablename__ = "executive_metrics"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    metric_name = Column(String)  # MTTR, Coverage %
    metric_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)


class ForecastData(Base):
    __tablename__ = "forecast_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    forecast_category = Column(String)  # Asset Growth, Risk Trends
    projected_value = Column(Float)
    target_date = Column(DateTime)
    timestamp = Column(DateTime, default=datetime.utcnow)


class ExposureMetric(Base):
    __tablename__ = "exposure_metrics"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    exposure_score = Column(Float, default=0.0)  # 0-100
    timestamp = Column(DateTime, default=datetime.utcnow)


class RiskMetric(Base):
    __tablename__ = "risk_metrics"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    risk_score = Column(Float, default=0.0)  # 0-100
    timestamp = Column(DateTime, default=datetime.utcnow)





def get_analytics_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
