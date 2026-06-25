import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from reconx.database.models import Scan
from reconx.database.session import async_session_factory


class ScanService:
    def __init__(self, db_session: AsyncSession | None = None):
        self.db_session = db_session

    async def create_scan(self, project_id: str, target_id: str, scan_type: str) -> Scan:
        scan = Scan(
            id=str(uuid.uuid4()),
            project_id=project_id,
            target_id=target_id,
            scan_type=scan_type,
            status="pending",
        )
        if self.db_session:
            self.db_session.add(scan)
            await self.db_session.commit()
            return scan

        async with async_session_factory() as db:
            db.add(scan)
            await db.commit()
            return scan

    async def scan_status(self, scan_id: str) -> Scan | None:
        stmt = select(Scan).where(Scan.id == scan_id)
        if self.db_session:
            result = await self.db_session.execute(stmt)
            return result.scalar_one_or_none()

        async with async_session_factory() as db:
            result = await db.execute(stmt)
            return result.scalar_one_or_none()


scan_service = ScanService()
