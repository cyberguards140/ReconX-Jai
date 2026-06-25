from data.database.models import Project
from data.database.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    pass


project_repo = ProjectRepository(Project)
