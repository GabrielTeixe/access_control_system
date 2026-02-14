from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.models.user import User
from src.models.role import Role
from src.database.session import get_db
from src.core.deps import get_current_user
from src.core.security import get_password_hash
from src.core.permissions import require_admin


router = APIRouter(prefix="/users", tags=["Users"])
templates = Jinja2Templates(directory="src/templates")


# SOMENTE ADMIN
def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    if not current_user.role or current_user.role.name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )

    return current_user


# LISTAR USUÁRIOS
@router.get("/")
def list_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    users = db.query(User).order_by(User.id.desc()).all()

    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users
        }
    )


# CRIAR USUÁRIO
@router.post("/add")
def add_user(
    fullname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role_name: str = Form("user"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Usuário já existe")

    role = db.query(Role).filter(Role.name == role_name).first()

    if not role:
        raise HTTPException(status_code=400, detail="Role inválida")

    new_user = User(
        name=fullname,
        email=email,
        password=get_password_hash(password),
        role=role,
        is_active=True
    )

    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/users/", status_code=status.HTTP_303_SEE_OTHER)


# DELETAR
@router.get("/delete/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode deletar a si mesmo"
        )

    db.delete(user)
    db.commit()

    return RedirectResponse(url="/users/", status_code=status.HTTP_303_SEE_OTHER)


# ATIVAR / DESATIVAR
@router.get("/toggle/{user_id}")
def toggle_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode desativar a si mesmo"
        )

    user.is_active = not user.is_active
    db.commit()

    return RedirectResponse(url="/users/", status_code=status.HTTP_303_SEE_OTHER)


# ALTERAR FUNÇÃO
@router.get("/role/{user_id}")
def change_role(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode alterar sua própria função"
        )

    new_role_name = "admin" if user.role.name == "user" else "user"
    new_role = db.query(Role).filter(Role.name == new_role_name).first()

    user.role = new_role
    db.commit()

    return RedirectResponse(url="/users/", status_code=status.HTTP_303_SEE_OTHER)


# API
@router.get("/all")
def get_users_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(User).all()
