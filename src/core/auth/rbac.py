from core.legacy_core.auth_db import Permission, Role, SessionLocal, User


class RBACEngine:
    @staticmethod
    def check_permission(user_id, required_permission):
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            db.close()
            return False

        # Super admin bypass
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if role and role.name == "Super Admin":
            db.close()
            return True

        perms = db.query(Permission).filter(Permission.role_id == user.role_id).all()
        has_perm = any(p.permission == required_permission for p in perms)
        db.close()
        return has_perm
