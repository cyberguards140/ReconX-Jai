import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "workspace", "intelligence.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class UniversalAsset(Base):
    __tablename__ = "assets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String)
    asset_type = Column(String)  # domain, ip, port, url, endpoint, finding, etc.
    value = Column(String, index=True)
    risk_score = Column(Integer, default=0)
    created = Column(DateTime, default=datetime.utcnow)


class Relationship(Base):
    __tablename__ = "relationships"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("assets.id"))
    target_id = Column(String, ForeignKey("assets.id"))
    relation_type = Column(String)  # RESOLVES_TO, HOSTS, USES, RUNS
    created = Column(DateTime, default=datetime.utcnow)


class AssetTag(Base):
    __tablename__ = "asset_tags"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, ForeignKey("assets.id"))
    tag = Column(String, index=True)


class AssetTimeline(Base):
    __tablename__ = "asset_timeline"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, ForeignKey("assets.id"))
    event_type = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AssetNote(Base):
    __tablename__ = "asset_notes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, ForeignKey("assets.id"))
    note = Column(Text)
    created = Column(DateTime, default=datetime.utcnow)


class AssetSearchIndex(Base):
    __tablename__ = "asset_search_index"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, ForeignKey("assets.id"))
    searchable_text = Column(Text)


Base.metadata.create_all(bind=engine)


def get_intelligence_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
