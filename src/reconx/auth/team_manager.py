from core.auth_db import SessionLocal, Team, TeamMember


class TeamManager:
    @staticmethod
    def create_team(org_id, name):
        db = SessionLocal()
        t = Team(organization_id=org_id, name=name)
        db.add(t)
        db.commit()
        db.refresh(t)
        t_id = t.id
        db.close()
        return t_id

    @staticmethod
    def assign_user(team_id, user_id):
        db = SessionLocal()
        tm = TeamMember(team_id=team_id, user_id=user_id)
        db.add(tm)
        db.commit()
        db.close()
