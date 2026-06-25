from reconx.database.models import Scan
from reconx.database.repositories.base import BaseRepository


class ScanRepository(BaseRepository[Scan]):
    pass


scan_repo = ScanRepository(Scan)
