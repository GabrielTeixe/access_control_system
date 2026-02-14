from src.database.session import SessionLocal


from src.models.user import User
from src.models.role import Role
from src.models.permission import Permission
from src.models.role_permission import role_permissions

from src.core.security import get_password_hash


def create_admin():
    db = SessionLocal()

    # Verifica se já existe
    admin = db.query(User).filter(User.email == "admin@admin.com").first()
    if admin:
        print("Admin já existe!")
        db.close()
        return

    # Busca role admin
    role_admin = db.query(Role).filter(Role.name == "admin").first()

    if not role_admin:
        role_admin = Role(name="admin")
        db.add(role_admin)
        db.commit()
        db.refresh(role_admin)

    # Cria usuário admin
    admin = User(
        name="Administrador",
        email="admin@admin.com",
        password=get_password_hash("1234"),
        role=role_admin
    )

    db.add(admin)
    db.commit()
    db.close()

    print("Admin criado com sucesso!")
    print("Email: admin@admin.com")
    print("Senha: 1234")


if __name__ == "__main__":
    create_admin()
