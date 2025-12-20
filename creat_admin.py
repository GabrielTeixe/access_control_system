# create_admin.py
from src.database.session import SessionLocal
from src.models.user import User  # ajuste para o caminho do seu modelo de usuário
from passlib.context import CryptContext

# Configuração de hash de senha (usando bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_admin():
    db = SessionLocal()

    # Verifica se já existe um admin
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        print("Admin já existe!")
        db.close()
        return

    novo_admin = User(
        username="admin",
        email="admin@teste.com",
        password=hash_password("1234"),  # senha do admin
        is_active=True,
        is_superuser=True  # se o seu modelo tiver
    )

    db.add(novo_admin)
    db.commit()
    db.close()
    print("Admin criado com sucesso! Usuário: admin | Senha: 1234")

if __name__ == "__main__":
    create_admin()
