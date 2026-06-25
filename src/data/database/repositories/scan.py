from data.database.models import Scan
from data.database.repositories.base import BaseRepository


class ScanRepository(BaseRepository[Scan]):
    pass


scan_repo = ScanRepository(Scan)
