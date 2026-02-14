from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.models.role import Role
from src.models.user import User
from src.database.session import get_db
from src.core.deps import get_current_user
from src.core.permissions import require_admin


router = APIRouter(prefix="/roles", tags=["Roles"])
templates = Jinja2Templates(directory="src/templates")


# Verificação simples de admin
def require_admin(user: User):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuário Inativo")

    if user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")


# LISTAR ROLES
@router.get("/")
def list_roles(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    # Busca roles + quantidade de usuários
    roles = (
        db.query(
            Role,
            func.count(User.id).label("user_count")
        )
        .outerjoin(User, User.role_id == Role.id)
        .group_by(Role.id)
        .order_by(Role.id.desc())
        .all()
    )

    return templates.TemplateResponse(
        "roles.html",
        {
            "request": request,
            "roles": roles
        }
    )


# CRIAR ROLE
@router.post("/add")
def add_role(
    name: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    existing_role = db.query(Role).filter(Role.name == name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role já existe")

    new_role = Role(name=name, is_active=True)

    db.add(new_role)
    db.commit()

    return RedirectResponse(url="/roles/", status_code=303)


# DELETAR ROLE
@router.post("/delete")
def delete_role(
    role_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    role = db.get(Role, role_id)

    if not role:
        raise HTTPException(status_code=404, detail="Role não encontrada")

    # Impede deletar role com usuários vinculados
    user_count = db.query(User).filter(User.role_id == role.id).count()
    if user_count > 0:
        raise HTTPException(
            status_code=400,
            detail="Não é possível excluir uma role com usuários vinculados"
        )

    db.delete(role)
    db.commit()

    return RedirectResponse(url="/roles/", status_code=303)


#  API
@router.get("/all")
def get_roles_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    require_admin(current_user)

    return db.query(Role).all()
