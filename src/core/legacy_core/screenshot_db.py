import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "workspace", "screenshots.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Screenshot(Base):
    __tablename__ = "screenshots"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class OCRResult(Base):
    __tablename__ = "ocr_results"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    text = Column(Text)


class LoginPage(Base):
    __tablename__ = "login_pages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    type = Column(String)  # SSO, Basic, OAuth


class VisualFinding(Base):
    __tablename__ = "visual_findings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    finding_type = Column(String)  # Exposed Admin, Default Dashboard


class Fingerprint(Base):
    __tablename__ = "fingerprints"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    technology = Column(String)


class VisualChange(Base):
    __tablename__ = "visual_changes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String)
    change_score = Column(Float)
    prev_screenshot_id = Column(String)


Base.metadata.create_all(bind=engine)


def get_screenshot_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
