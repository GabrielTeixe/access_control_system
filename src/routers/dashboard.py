from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.models.user import User
from src.models.audit import Audit
from src.core.permissions import require_admin


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):

    # USERS
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = total_users - active_users

    # AUDIT LOGS
    total_entries = db.query(Audit).count()
    last_entries = (
        db.query(Audit)
        .order_by(Audit.id.desc())
        .limit(5)
        .all()
    )

    stats = {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": inactive_users,
        "total_entries": total_entries,
    }

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "current_user": current_user,
            "stats": stats,
            "last_entries": last_entries
        }
    )
