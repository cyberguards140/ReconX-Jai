from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Dict, Any, List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
import json

from apps.api_gateway.gateway.router_registry import registry
from data.database.repositories.project import project_repo
from data.database.models import Project
from data.database.session import get_db

router = APIRouter()
registry.register(router, prefix="/projects", version="v1", tags=["projects"])

ACTIVE_PROJECT_ID = None

class ProjectCreate(BaseModel):
    name: str
    description: str = ""

class ProjectSwitch(BaseModel):
    name: str

@router.get("/")
async def get_projects(db: AsyncSession = Depends(get_db)):
    projects = await project_repo.get_multi(db)
    return [{"id": p.id, "name": p.name, "description": p.description} for p in projects]

@router.get("/active")
async def get_active_project(db: AsyncSession = Depends(get_db)):
    global ACTIVE_PROJECT_ID
    if not ACTIVE_PROJECT_ID:
        return {"project": None}
    p = await project_repo.get(db, ACTIVE_PROJECT_ID)
    if not p:
        return {"project": None}
    config = json.loads(p.config) if isinstance(p.config, str) else (p.config or {})
    return {"project": p.name, "id": p.id, "description": p.description, "config": config}

class ProjectConfigUpdate(BaseModel):
    config: Dict[str, Any]

@router.post("/active/config")
async def update_active_config(data: ProjectConfigUpdate, db: AsyncSession = Depends(get_db)):
    global ACTIVE_PROJECT_ID
    if not ACTIVE_PROJECT_ID:
        raise HTTPException(status_code=400, detail="No active project")
    p = await project_repo.get(db, ACTIVE_PROJECT_ID)
    if not p:
        raise HTTPException(status_code=400, detail="Active project not found in DB")
    
    current_config = json.loads(p.config) if isinstance(p.config, str) else (p.config or {})
    current_config.update(data.config)
    
    await project_repo.update(db, db_obj=p, obj_in={"config": current_config})
    return {"status": "ok", "config": current_config}

@router.post("/create")
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project_id = str(uuid.uuid4())
    p = await project_repo.create(db, obj_in={"id": project_id, "name": data.name, "description": data.description, "owner_id": "system"})
    return {"status": "ok", "id": p.id}

@router.post("/switch")
async def switch_project(data: ProjectSwitch, db: AsyncSession = Depends(get_db)):
    global ACTIVE_PROJECT_ID
    projects = await project_repo.get_multi(db)
    for p in projects:
        if p.name == data.name:
            ACTIVE_PROJECT_ID = p.id
            return {"status": "ok", "id": p.id}
    raise HTTPException(status_code=404, detail="Project not found")

@router.delete("/delete")
async def delete_project(data: ProjectSwitch, db: AsyncSession = Depends(get_db)):
    global ACTIVE_PROJECT_ID
    projects = await project_repo.get_multi(db)
    for p in projects:
        if p.name == data.name:
            await project_repo.delete(db, id=p.id)
            if ACTIVE_PROJECT_ID == p.id:
                ACTIVE_PROJECT_ID = None
            return {"status": "ok"}
    raise HTTPException(status_code=404, detail="Project not found")
