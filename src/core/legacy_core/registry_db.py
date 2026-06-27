import os

from sqlalchemy import JSON, Boolean, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.abspath(
    os.path.join(os.path.expanduser("~/ReconX/registry"), "registry.db")
)
import os; os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True)
    name = Column(String)
    order = Column(Integer)


class Tool(Base):
    __tablename__ = "tools"
    id = Column(String, primary_key=True)
    name = Column(String)
    category_id = Column(String, ForeignKey("categories.id"))
    description = Column(String, default="")
    version = Column(String, default="latest")
    binary = Column(String, default="")
    execution_type = Column(String, default="local")
    live_terminal = Column(Boolean, default=True)
    enabled = Column(Boolean, default=True)
    tags = Column(JSON, default=list)


class ToolArgument(Base):
    __tablename__ = "tool_arguments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tool_id = Column(String, ForeignKey("tools.id"))
    flag = Column(String)
    type = Column(String)  # toggle, textbox, dropdown, etc.
    default_value = Column(String, default="")


class ToolDependency(Base):
    __tablename__ = "tool_dependencies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tool_id = Column(String, ForeignKey("tools.id"))
    dep_type = Column(String)  # binary, python, pip, system
    name = Column(String)


class ToolProfile(Base):
    __tablename__ = "tool_profiles"
    id = Column(String, primary_key=True)
    tool_id = Column(String, ForeignKey("tools.id"))
    name = Column(String)
    arguments_json = Column(JSON)


class ToolTemplate(Base):
    __tablename__ = "tool_templates"
    id = Column(String, primary_key=True)
    name = Column(String)
    tools_json = Column(JSON)





def get_registry_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
