from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates
from src.frontend.dependencies import *
from src.users.models import Users


router = APIRouter(
    tags=["frontend endpoint"]
)

templates = Jinja2Templates('src/frontend/public')

@router.get("/")
async def main_endpoint(
    user: Users = Depends(get_current_user)
):
    if user:
        return RedirectResponse("/dashboard")
    return RedirectResponse("/auth")


@router.get("/auth")
async def index(request: Request, user: Users = Depends(get_current_user)):
    if user == None:
        return templates.TemplateResponse("auth.html", {"request": request})    
    return RedirectResponse("/dashboard")


@router.get("/dashboard")
async def dashboard(request: Request, user: Users = Depends(get_current_user)):
    if user == None:
        return RedirectResponse("/auth")
    return templates.TemplateResponse("dashboard.html", {"request": request, "data": user})
