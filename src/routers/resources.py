from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.models.resource import Resource
from src.models.user import User
from src.core.permissions import require_admin


router = APIRouter(prefix="/resources", tags=["Resources"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/")
def list_resources(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    resources = db.query(Resource).order_by(Resource.id.desc()).all()

    return templates.TemplateResponse(
        "resources.html",
        {
            "request": request,
            "resources": resources
        }
    )


@router.post("/add")
def add_resource(
    name: str = Form(...),
    path: str = Form(...),
    type: str = Form(...),
    required_role: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    if db.query(Resource).filter(Resource.path == path).first():
        raise HTTPException(status_code=400, detail="Path já cadastrada")

    new_resource = Resource(
        name=name,
        path=path,
        type=type,
        required_role=required_role,
        is_active=True
    )

    db.add(new_resource)
    db.commit()

    return RedirectResponse(url="/resources/", status_code=303)


@router.post("/delete")
def delete_resource(
    resource_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    resource = db.get(Resource, resource_id)

    if not resource:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")

    db.delete(resource)
    db.commit()

    return RedirectResponse(url="/resources/", status_code=303)
