class TeamManagerService:
    def __init__(self):
        self.teams = []
        
    def add_team(self, team: dict):
        self.teams.append(team)
