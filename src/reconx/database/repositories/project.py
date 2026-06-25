from reconx.database.models import Project
from reconx.database.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    pass


project_repo = ProjectRepository(Project)
