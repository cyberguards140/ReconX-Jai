import os
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "workspace", "plugins.db")
)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Plugin(Base):
    __tablename__ = "plugins"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True)
    version = Column(String)
    author = Column(String)
    description = Column(Text)
    status = Column(String, default="Disabled")  # Enabled, Disabled, Installed
    category = Column(String)  # Tool, Theme, Connector
    installed_at = Column(DateTime, default=datetime.utcnow)


class PluginPermission(Base):
    __tablename__ = "plugin_permissions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    plugin_id = Column(String, ForeignKey("plugins.id"))
    permission = Column(String)  # assets.read, system.execute


class MarketplacePackage(Base):
    __tablename__ = "marketplace_packages"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    package_name = Column(String)
    version = Column(String)
    category = Column(String)
    author = Column(String)
    description = Column(Text)
    downloads = Column(Integer, default=0)


class ConnectorRegistry(Base):
    __tablename__ = "connector_registry"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    connector_name = Column(String)
    category = Column(String)  # SIEM, Ticketing, Messaging
    enabled = Column(Boolean, default=False)
    config = Column(Text)  # JSON configuration


class ThemeRegistry(Base):
    __tablename__ = "theme_registry"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    theme_name = Column(String)
    is_active = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


def get_plugin_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
