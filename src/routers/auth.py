from fastapi import APIRouter, Request, Form, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

# Banco de dados simulado
fake_users = {"admin": {"password": "1234", "full_name": "Administrador", "email": "admin@example.com", "role": "admin"}}

# LOGIN

@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_post(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    user = fake_users.get(username)
    if user and user["password"] == password:
        # Cria cookie de sessão
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="user", value=username)
        return response
    else:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Usuário ou senha incorretos"})

# REGISTER

@router.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    role: str = Form(...)
):
    if username in fake_users:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Usuário já existe"})
    
    # Adiciona usuário ao "banco"
    fake_users[username] = {
        "password": password,
        "full_name": full_name,
        "email": email,
        "role": role
    }
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
