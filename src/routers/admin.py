from fastapi import APIRouter,Request,Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.auth.jwt import required_admin
from src.core.permissions import require_admin


router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="src/templates")

@router.get("/panel",response_class=HTMLResponse)
def admin_panel(
    request: Request,
    current_user = Depends(required_admin)
):
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "current_user": current_user
        }
    )