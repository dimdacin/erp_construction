# main_web.py - Application web complète ERP Construction

from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from typing import Optional

from database import get_db
from models import *
from api_routes import router as api_router

# --- Initialisation de l'Application ---
app = FastAPI(title="ERP Construction - Application Web")

# Ajouter le middleware de session pour la gestion de connexion
app.secret_key = "votre-clé-secrète-très-longue-et-sécurisée-123456"
app.add_middleware(SessionMiddleware, secret_key=app.secret_key)

# Monter les fichiers statiques et templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inclure les routes API
app.include_router(api_router)

# Utilisateur fictif pour la démo (à remplacer par une vraie authentification)
USERS = {
    "admin": "admin123",
    "user": "user123"
}

# --- Middleware pour vérifier la connexion ---
def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return None
    return user

# --- Routes Web Frontend ---

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Page d'accueil - redirige vers login ou dashboard."""
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Page de connexion."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Traitement de la connexion."""
    if username in USERS and USERS[username] == password:
        request.session["user"] = username
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Nom d'utilisateur ou mot de passe incorrect"
    })

@app.get("/logout")
async def logout(request: Request):
    """Déconnexion."""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Tableau de bord principal."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    # Statistiques rapides
    total_sites = db.query(Site).count()
    total_equipements = db.query(Equipement).count()
    total_personnel = db.query(Personne).count()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "total_sites": total_sites,
        "total_equipements": total_equipements,
        "total_personnel": total_personnel
    })

@app.get("/sites", response_class=HTMLResponse)
async def sites_page(request: Request, db: Session = Depends(get_db)):
    """Page de liste des sites/chantiers."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("sites.html", {
        "request": request,
        "user": user
    })

@app.get("/equipements", response_class=HTMLResponse)
async def equipements_page(request: Request, db: Session = Depends(get_db)):
    """Page de liste des équipements."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("equipements.html", {
        "request": request,
        "user": user
    })

@app.get("/personnel", response_class=HTMLResponse)
async def personnel_page(request: Request, db: Session = Depends(get_db)):
    """Page de liste du personnel."""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("personnel.html", {
        "request": request,
        "user": user
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

