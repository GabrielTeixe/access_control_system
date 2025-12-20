from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Usuários com senha já hasheada (senha = 123)
USERS = {
    "admin": "$2b$12$N2bVj9KfWZjUz3cYFxF1zu7N8b4z1D/6Y8o8bVmpC6D8U8w5Z1y3S"
}

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    hashed_password = USERS.get(username)

    if not hashed_password or not pwd_context.verify(password, hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Usuário ou senha incorretos"}
        )

    # Redireciona para o dashboard
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="user", value=username)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/auth/login", status_code=303)
    response.delete_cookie(key="user")
    return response
