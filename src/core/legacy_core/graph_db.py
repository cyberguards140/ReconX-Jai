import os
import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "..", "workspace", "knowledge_graph.db"
    )
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class GraphEntity(Base):
    __tablename__ = "entities"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    entity_type = Column(String)  # Domain, IP, Subdomain, Port, Service, Technology
    entity_value = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class GraphRelationship(Base):
    __tablename__ = "relationships"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    source_id = Column(String, ForeignKey("entities.id"))
    target_id = Column(String, ForeignKey("entities.id"))
    relation_type = Column(String)  # RESOLVES_TO, USES, HOSTS, OWNS, LINKED_TO
    confidence_score = Column(Float, default=100.0)  # 0-100
    created_at = Column(DateTime, default=datetime.utcnow)


class AttackPath(Base):
    __tablename__ = "attack_paths"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    path_details = Column(Text)  # JSON representation of the traversal nodes
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Investigation(Base):
    __tablename__ = "investigations"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String, index=True)
    title = Column(String)
    status = Column(String, default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)


class InvestigationNote(Base):
    __tablename__ = "investigation_notes"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    investigation_id = Column(String, ForeignKey("investigations.id"))
    author = Column(String)
    note = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_graph_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
