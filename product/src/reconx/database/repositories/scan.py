from reconx.database.repositories.base import BaseRepository
from reconx.database.models import Scan


class ScanRepository(BaseRepository[Scan]):
    pass


scan_repo = ScanRepository(Scan)
