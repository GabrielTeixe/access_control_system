from fastapi import APIRouter, Form, Request,Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict

from src.auth.jwt import get_current_user
from src.core.audit import log_action
from src.core.permissions import require_admin


router = APIRouter(prefix="/access", tags=["Access"])
templates = Jinja2Templates(directory="src/templates")

#Banco Simulado
resources_db: List[Dict] = []

#Html

@router.get("/")
def list_resources(request: Request):
    return templates.TemplateResponse(
        "access.html",
        {"request": request, "resources": resources_db}
    )

@router.post("/add")
def add_resource(description: str = Form(...)):
    new_id = len(resources_db) + 1
    resources_db.append({"id": new_id, "description": description})
    return RedirectResponse(url = "/access/",status_code=302)

@router.post("/delete")
def delete_resource(resource_id: int = Form(...)):
    global resources_db
    resources_db = [r for r in resources_db if r["id"] == resource_id]
    return RedirectResponse(url= "/access/", status_code=302)

@router.get("/edit")
def edit_resource_get(request: Request, resource_id: int):
    res =next((r for r in resources_db if r["id"] == resource_id), None)
    if not res:
        return RedirectResponse(url="/access/")
    return templates.TemplateResponse(
        "edit_access.html",
        {"request": request, "resource": res}
    )

@router.post("/edit")
def edit_resource_post(resource_id: int = Form(...), description : str = Form(...)):
    for r in resources_db:
        if r["id"] == resource_id:
            r["description"] = description
            break
        return RedirectResponse("/access/", status_code=302)

#Controle de Entrada

@router.post("/enter")
def register_entry(current_user=Depends(get_current_user)):

    if not current_user["is_active"]:
        raise HTTPException(status_code=403, detail="Usuário Inativo")
    
    register_audit(current_user["username"], "Entrada")

    return {
        "status": "ok",
        "user": current_user["username"]
    }
