from src.database.session import SessionLocal
from src.models.role import Role
from src.models.user import User
from src.core.security import get_password_hash

db = SessionLocal()

# Criar roles
admin_role = Role(name="admin", is_active=True)
user_role = Role(name="user", is_active=True)

db.add(admin_role)
db.add(user_role)
db.commit()

# Criar admin
admin_user = User(
    name="Administrador",
    email="admin@email.com",
    password=get_password_hash("123456"),
    is_active=True,
    role_id=admin_role.id
)

db.add(admin_user)
db.commit()

db.close()

print("Banco populado com sucesso.")
