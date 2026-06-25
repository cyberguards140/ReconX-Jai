from data.database.models import Finding
from data.database.repositories.base import BaseRepository


class FindingRepository(BaseRepository[Finding]):
    pass


finding_repo = FindingRepository(Finding)
