from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.models.audit import Audit
from src.models.user import User
from src.core.permissions import require_admin

router = APIRouter(prefix="/audit", tags=["Audit"])
templates = Jinja2Templates(directory="src/templates")


# HTML — LISTAR LOGS

@router.get("/")
def list_logs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    logs = db.query(Audit).order_by(Audit.id.desc()).all()

    return templates.TemplateResponse(
        "audit.html",
        {
            "request": request,
            "logs": logs
        }
    )


# API — TODOS LOGS
@router.get("/all")
def get_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    return db.query(Audit).all()

# RELATÓRIO DIÁRIO
@router.get("/daily")
def daily_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    logs = db.query(Audit).all()

    return {
        "total": len(logs),
        "logs": logs
    }
