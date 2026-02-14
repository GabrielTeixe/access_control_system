from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.core.permissions import require_admin
from src.models.user import User
from src.models.role import Role
from src.database.session import get_db
from src.core.security import (
    create_access_token,
    get_password_hash,
    verify_password
)

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="src/templates")

# LOGIN

@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: str | None = Form(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "E-mail ou senha inválidos"
            }
        )

    token = create_access_token({"sub": user.email})

    response = RedirectResponse(
        url="/dashboard/",
        status_code=303
    )

    response.set_cookie(
        key="access_token",
        value=token,
        max_age=60 * 60 * 24 * 7 if remember else None,
        httponly=True,
        samesite="lax",
        path="/"
    )

    return response

# REGISTER

@router.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )


@router.post("/register")
def register_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Verifica se já existe
    exists = db.query(User).filter(User.email == email).first()

    if exists:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Usuário já existe"
            }
        )

    # Busca a role padrão "user"
    user_role = db.query(Role).filter(Role.name == "user").first()

    if not user_role:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "Role 'user' não encontrada no banco"
            }
        )

    # Cria usuário
    user = User(
        name=name,
        email=email,
        password=get_password_hash(password),
        is_active=True,
        role_id=user_role.id
    )

    db.add(user)
    db.commit()

    return RedirectResponse(url="/auth/login", status_code=303)

# LOGOUT

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth/login", status_code=302)
    response.delete_cookie("access_token", path="/")
    return response
