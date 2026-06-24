import os
from sqlalchemy import create_engine, Column, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'workspace', 'threat_intelligence.db'))
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class CVEData(Base):
    __tablename__ = "cve_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    cve = Column(String, index=True)
    severity = Column(String)
    cvss = Column(Float)
    created = Column(DateTime, default=datetime.utcnow)

class IOCData(Base):
    __tablename__ = "iocs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    ioc_type = Column(String) # ip, domain, url, hash
    value = Column(String, index=True)
    source = Column(String)
    created = Column(DateTime, default=datetime.utcnow)

class ReputationData(Base):
    __tablename__ = "reputation"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    reputation_score = Column(Float)
    status = Column(String) # trusted, suspicious, malicious
    created = Column(DateTime, default=datetime.utcnow)

class PassiveDNS(Base):
    __tablename__ = "passive_dns"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    domain = Column(String, index=True)
    historical_ip = Column(String)
    created = Column(DateTime, default=datetime.utcnow)

class ASNData(Base):
    __tablename__ = "asn_data"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    asn = Column(String)
    organization = Column(String)
    country = Column(String)
    created = Column(DateTime, default=datetime.utcnow)

class ExposureEvent(Base):
    __tablename__ = "exposure_events"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    event_type = Column(String) # new_public_port, new_secret
    created = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_threat_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
