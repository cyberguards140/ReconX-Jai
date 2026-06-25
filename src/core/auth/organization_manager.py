from core.legacy_core.auth_db import Organization, SessionLocal


class OrganizationManager:
    @staticmethod
    def create_organization(name):
        db = SessionLocal()
        org = Organization(name=name)
        db.add(org)
        db.commit()
        db.refresh(org)
        org_id = org.id
        db.close()
        return org_id

    @staticmethod
    def get_organizations():
        db = SessionLocal()
        orgs = db.query(Organization).all()
        res = [{"id": o.id, "name": o.name} for o in orgs]
        db.close()
        return res
