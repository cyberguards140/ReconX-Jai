from reconx.database.repositories.base import BaseRepository
from reconx.database.models import Project


class ProjectRepository(BaseRepository[Project]):
    pass


project_repo = ProjectRepository(Project)
