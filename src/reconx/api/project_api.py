import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from project_manager.project_service import ProjectService

project_service = ProjectService()

class ProjectAPI:
    def handle_request(self, method, path, data=None):
        parts = path.strip('/').split('/')
        if len(parts) >= 2 and parts[0] == 'api' and parts[1] == 'projects':
            
            if len(parts) == 2 and method == 'POST':
                name = data.get("name")
                tags = data.get("tags", [])
                return project_service.create_project(name, tags)
                
            if len(parts) == 3 and method == 'GET':
                return {"status": "loaded", "project_id": parts[2]}
                
            if len(parts) == 4 and parts[3] == 'export' and method == 'POST':
                return {"status": "exported"}
                
        return {"error": "Invalid project endpoint"}
