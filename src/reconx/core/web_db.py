import os
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'workspace', 'web_assets.db'))
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class WebAsset(Base):
    __tablename__ = "web_assets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_type = Column(String) # url, directory, file, parameter, endpoint, js_file
    value = Column(String)
    source = Column(String)
    host = Column(String)
    project_id = Column(String)
    status = Column(Integer, nullable=True) # e.g. 200, 404
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

class Secret(Base):
    __tablename__ = "secrets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category = Column(String)
    value = Column(Text)
    source_id = Column(String, ForeignKey("web_assets.id"), nullable=True)
    project_id = Column(String)

class Technology(Base):
    __tablename__ = "technologies"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    host = Column(String)
    project_id = Column(String)

class WebRelationship(Base):
    __tablename__ = "web_relationships"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String, ForeignKey("web_assets.id"))
    target_id = Column(String, ForeignKey("web_assets.id"))

Base.metadata.create_all(bind=engine)

def get_web_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
