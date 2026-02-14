from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# DATABASE
from src.database.session import engine, SessionLocal
from src.database.base import Base

from src.models.user import User
from src.models.role import Role
from src.models.permission import Permission
from src.models.role_permission import role_permissions
from src.models.access_log import AccessLog
from src.models.audit import Audit

from src.core.security import get_password_hash

# ROUTERS
from src.routers import admin
from src.routers import auth, users, access, audit, roles, dashboard
from src.routers import resources


# APP CONFIG

app = FastAPI(
    title="Access Control & Audit System",
    version="1.0.0",
    description="Sistema de controle de acesso com auditoria"
)

# CRIA TABELAS

Base.metadata.create_all(bind=engine)


# INIT ROLES + ADMIN

def init_system():
    db = SessionLocal()

    # Garantir roles

    admin_role = db.query(Role).filter(Role.name == "admin").first()
    user_role = db.query(Role).filter(Role.name == "user").first()

    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()
        db.refresh(admin_role)

    if not user_role:
        user_role = Role(name="user")
        db.add(user_role)
        db.commit()
        db.refresh(user_role)

    # Garantir usuário admin

    admin_user = db.query(User).filter(User.email == "admin@admin.com").first()

    if not admin_user:
        new_admin = User(
            name="Administrador",
            email="admin@admin.com",
            password=get_password_hash("123456"),
            role_id=admin_role.id,
            is_active=True
        )
        db.add(new_admin)
        db.commit()

    db.close()


init_system()

# TEMPLATES E STATIC

templates = Jinja2Templates(directory="src/templates")

app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static"
)

# ROOT

@app.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse(url="/dashboard")

# ROUTERS

app.include_router(resources.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(access.router)
app.include_router(audit.router)
app.include_router(roles.router)
app.include_router(dashboard.router)
