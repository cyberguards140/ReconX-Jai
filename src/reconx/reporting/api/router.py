import os
import uuid

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from reconx.api.dependencies import get_current_user, require_permission
from reconx.database.models import ReportRecord, ReportSchedule, User
from reconx.database.session import get_db
from reconx.reporting.engine.distributor import ReportDistributor
from reconx.reporting.engine.report_engine import ReportEngine

router = APIRouter(prefix="/reports", tags=["Reporting"])

# We locate templates in the parent's sibling directory 'templates'
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
report_engine = ReportEngine(templates_dir=TEMPLATES_DIR)


class GenerateReportRequest(BaseModel):
    target_scope: str
    report_type: str = "Executive"  # "Executive" or "Technical"
    export_format: str = "pdf"  # "pdf", "html", "json", "csv"
    title: str = "ReconX Report"
    distribute_to: list[dict] | None = None
    report_data: dict | None = None  # For injecting specific data


class ReportScheduleRequest(BaseModel):
    report_type: str
    cron_expression: str
    distribute_to: list[dict] | None = None


@router.post(
    "/generate", response_model=dict, dependencies=[Depends(require_permission("report.generate"))]
)
async def generate_report(
    request: GenerateReportRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate an intelligence report.
    """
    if request.report_type == "Executive":
        if request.export_format not in ["pdf", "html", "json"]:
            raise HTTPException(status_code=400, detail="Invalid format for Executive report")
        record = await report_engine.generate_executive_report(
            session=db,
            target_scope=request.target_scope,
            title=request.title,
            export_format=request.export_format,
            report_data=request.report_data,
        )
    elif request.report_type == "Technical":
        if request.export_format not in ["json", "csv"]:
            raise HTTPException(status_code=400, detail="Invalid format for Technical report")
        record = await report_engine.generate_technical_report(
            session=db,
            target_scope=request.target_scope,
            title=request.title,
            export_format=request.export_format,
            report_data=request.report_data,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

    if request.distribute_to:
        background_tasks.add_task(
            ReportDistributor.distribute, record.report_id, request.distribute_to
        )

    return {
        "status": "success",
        "report_id": record.report_id,
        "file_path": record.metadata_json.get("file_path"),
    }


@router.get(
    "/", response_model=list[dict], dependencies=[Depends(require_permission("report.read"))]
)
async def list_reports(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    List all generated reports.
    """
    stmt = select(ReportRecord)
    result = await db.execute(stmt)
    records = result.scalars().all()

    return [
        {
            "report_id": r.report_id,
            "title": r.title,
            "report_type": r.report_type,
            "generated_at": r.generated_at,
            "metadata": r.metadata_json,
        }
        for r in records
    ]


@router.post(
    "/schedules", response_model=dict, dependencies=[Depends(require_permission("report.generate"))]
)
async def create_schedule(
    request: ReportScheduleRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new report schedule.
    """
    schedule_id = str(uuid.uuid4())
    schedule = ReportSchedule(
        id=schedule_id,
        report_type=request.report_type,
        tenant_id=current_user.tenant_id,
        cron_expression=request.cron_expression,
        distribute_to=request.distribute_to,
    )
    db.add(schedule)
    await db.commit()

    return {"status": "success", "schedule_id": schedule_id}


@router.get(
    "/schedules",
    response_model=list[dict],
    dependencies=[Depends(require_permission("report.read"))],
)
async def list_schedules(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """
    List report schedules.
    """
    stmt = select(ReportSchedule)
    if current_user.tenant_id:
        stmt = stmt.where(ReportSchedule.tenant_id == current_user.tenant_id)
    result = await db.execute(stmt)
    schedules = result.scalars().all()

    return [
        {
            "id": s.id,
            "report_type": s.report_type,
            "cron_expression": s.cron_expression,
            "next_run": s.next_run,
            "status": s.status,
        }
        for s in schedules
    ]
