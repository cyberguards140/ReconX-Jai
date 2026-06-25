import os
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "distributed.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Cluster(Base):
    __tablename__ = "clusters"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    cluster_type = Column(String)  # Recon, Vuln, Cloud, Web
    created = Column(DateTime, default=datetime.utcnow)


class Node(Base):
    __tablename__ = "nodes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    hostname = Column(String, unique=True)
    node_type = Column(String)  # Controller, Worker
    status = Column(String, default="Online")  # Online, Offline, Busy, Maintenance
    cluster_id = Column(String, ForeignKey("clusters.id"), nullable=True)
    created = Column(DateTime, default=datetime.utcnow)


class Agent(Base):
    __tablename__ = "agents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    node_id = Column(String, ForeignKey("nodes.id"))
    auth_token = Column(String, unique=True)
    version = Column(String)
    last_seen = Column(DateTime, default=datetime.utcnow)


class NodeCapability(Base):
    __tablename__ = "node_capabilities"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    node_id = Column(String, ForeignKey("nodes.id"))
    tool_name = Column(String)
    is_available = Column(Boolean, default=True)


class NodeHealth(Base):
    __tablename__ = "node_health"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    node_id = Column(String, ForeignKey("nodes.id"))
    cpu_usage = Column(Float)
    ram_usage = Column(Float)
    disk_usage = Column(Float)
    network_latency = Column(Float)
    health_state = Column(String, default="Healthy")  # Healthy, Warning, Critical
    timestamp = Column(DateTime, default=datetime.utcnow)


class DistributedJob(Base):
    __tablename__ = "distributed_jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_name = Column(String)
    payload = Column(Text)
    status = Column(String, default="Queued")  # Queued, Assigned, Running, Completed, Failed
    created = Column(DateTime, default=datetime.utcnow)


class JobAssignment(Base):
    __tablename__ = "job_assignments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("distributed_jobs.id"))
    node_id = Column(String, ForeignKey("nodes.id"))
    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    result_data = Column(Text, nullable=True)


Base.metadata.create_all(bind=engine)


def get_distributed_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
