from reconx.database.repositories.base import BaseRepository
from reconx.database.models import Target


class TargetRepository(BaseRepository[Target]):
    pass


target_repo = TargetRepository(Target)
