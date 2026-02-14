from src.database.session import SessionLocal
from src.models.role import Role


def init_roles():
    db = SessionLocal()

    admin_role = db.query(Role).filter(Role.name == "admin").first()
    user_role = db.query(Role).filter(Role.name == "user").first()

    if not admin_role:
        db.add(Role(name="admin", is_active=True))

    if not user_role:
        db.add(Role(name="user", is_active=True))

    db.commit()
    db.close()
