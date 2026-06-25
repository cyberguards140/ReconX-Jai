from reconx.database.models import Target
from reconx.database.repositories.base import BaseRepository


class TargetRepository(BaseRepository[Target]):
    pass


target_repo = TargetRepository(Target)
