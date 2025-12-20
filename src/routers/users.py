from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

# Lista simulada de usuários
users_list = [{"username": "admin"}]

@router.get("/", response_class=None)
def list_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users_list})

@router.post("/add")
def add_user(request: Request, username: str = Form(...)):
    # Evita duplicados
    if username not in [u["username"] for u in users_list]:
        users_list.append({"username": username})
    return RedirectResponse(url="/users", status_code=303)
