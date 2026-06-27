import os
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.expanduser("~/ReconX/workspace"), "cloud_assets.db")
)
import os; os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class CloudAsset(Base):
    __tablename__ = "cloud_assets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String)  # aws, azure, gcp
    service = Column(String)
    resource_type = Column(String)
    name = Column(String)
    public = Column(Boolean, default=False)
    project_id = Column(String)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)


class StorageBucket(Base):
    __tablename__ = "storage_buckets"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String)
    name = Column(String)
    public = Column(Boolean, default=False)
    object_count = Column(Integer, default=0)
    project_id = Column(String)


class IAMEntity(Base):
    __tablename__ = "iam_entities"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String)
    entity_type = Column(String)  # user, role, group, policy
    name = Column(String)
    project_id = Column(String)


class PublicExposure(Base):
    __tablename__ = "public_exposures"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    asset_id = Column(String, ForeignKey("cloud_assets.id"))
    finding = Column(String)
    severity = Column(String)
    project_id = Column(String)


class CloudRelationship(Base):
    __tablename__ = "cloud_relationships"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String)
    target_id = Column(String)





def get_cloud_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
