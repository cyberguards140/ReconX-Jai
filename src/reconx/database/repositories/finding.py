from reconx.database.repositories.base import BaseRepository
from reconx.database.models import Finding


class FindingRepository(BaseRepository[Finding]):
    pass


finding_repo = FindingRepository(Finding)
