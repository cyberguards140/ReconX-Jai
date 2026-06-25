from .project_index import ProjectIndex
from .workspace_loader import WorkspaceLoader

class ProjectService:
    def __init__(self):
        self.index = ProjectIndex()
        self.loader = WorkspaceLoader()
        
    def create_project(self, name, tags=None):
        project_id = self.index.create_project_record(name, tags)
        workspace_path = self.loader.create_workspace(name)
        return {"project_id": project_id, "name": name, "path": workspace_path}
