from reconx.database.models import Finding
from reconx.database.repositories.base import BaseRepository


class FindingRepository(BaseRepository[Finding]):
    pass


finding_repo = FindingRepository(Finding)
