import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dashboard_data.metrics_engine import MetricsEngine

metrics = MetricsEngine()

class DashboardAPI:
    def handle_request(self, method, path):
        parts = path.strip('/').split('/')
        if len(parts) >= 3 and parts[0] == 'api' and parts[1] == 'dashboard':
            
            if parts[2] == 'overview':
                return metrics.get_overview_counts()
                
            elif parts[2] == 'findings':
                return {"findings": []}
                
            elif parts[2] == 'assets':
                return {"assets": []}
                
            elif parts[2] == 'technologies':
                return {"technologies": []}
                
            elif parts[2] == 'activity':
                return {"activity": []}
                
            elif parts[2] == 'charts':
                return {"charts": []}
                
        return {"error": "Invalid dashboard endpoint"}
