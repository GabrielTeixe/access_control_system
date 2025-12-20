from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="src/templates")

# Lista simulada de logs de auditoria
logs_list = [
    {"user": "admin", "action": "Login", "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S")},
]

@router.get("/", response_class=None)
def list_logs(request: Request):
    return templates.TemplateResponse("audit.html", {"request": request, "logs": logs_list})
