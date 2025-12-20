from fastapi import FastAPI, Request, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from src.routers import auth  # certifique-se que auth.py está dentro de src/routers

app = FastAPI(title="Access Control & Audit System")

# Configura templates e static
templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# Inclui o router
app.include_router(auth.router, prefix="/auth")

# Página inicial redireciona para login
@app.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse(url="/auth/login")

# Dashboard
@app.get("/dashboard")
def dashboard(request: Request, user: str | None = Cookie(default=None)):
    if not user:
        return RedirectResponse(url="/auth/login")  # usuário não logado
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user}
    )
