import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.expanduser("~/ReconX/workspace"), "assets.db")
)
import os; os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Asset(Base):
    __tablename__ = "assets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_type = Column(String)  # domain, subdomain, ip, port, service, technology, vulnerability
    value = Column(String)
    source = Column(String)
    project_id = Column(String)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)


class Relationship(Base):
    __tablename__ = "relationships"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String)
    target_id = Column(String)
    relation_type = Column(String)  # e.g. "has_port", "resolves_to"


class AssetHistory(Base):
    __tablename__ = "asset_history"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    event_description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)





def get_asset_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
