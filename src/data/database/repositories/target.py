from data.database.models import Target
from data.database.repositories.base import BaseRepository


class TargetRepository(BaseRepository[Target]):
    pass


target_repo = TargetRepository(Target)
