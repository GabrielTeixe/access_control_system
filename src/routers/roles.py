from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

# Lista simulada de roles
roles_list = [{"name": "Administrador"}, {"name": "Usuário"}]

@router.get("/", response_class=None)
def list_roles(request: Request):
    return templates.TemplateResponse("roles.html", {"request": request, "roles": roles_list})

@router.post("/add")
def add_role(request: Request, name: str = Form(...)):
    if name not in [r["name"] for r in roles_list]:
        roles_list.append({"name": name})
    return RedirectResponse(url="/roles", status_code=303)
