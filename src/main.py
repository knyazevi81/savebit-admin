from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.clients.router import router as clients_router
from src.config import settings
from src.database import create_tables
from src.frontend.router import router as frontend_router
from src.servers.router import router as servers_router
from src.users.auth import get_password_hash
from src.users.router import router as user_admin_router
from src.users.service import UserService


class NotFoundRedirectMiddleware(BaseHTTPMiddleware):
    """
    Мидлварь для редиректа при попытке зайти в несуществующий эндопоинт
    просто редиректит в страницу аунтификации
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return RedirectResponse(url="/auth")
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    existing_user = await UserService.find_one_or_none(login=settings.PREREG_LOGIN)

    if not existing_user:
        hashed_password = get_password_hash(settings.PREREG_PASSWORD)
        await UserService.add(
            login=settings.PREREG_LOGIN, hashed_password=hashed_password
        )
    yield


def get_application() -> FastAPI:
    _app = FastAPI(title="Savebit admin panel API", lifespan=lifespan)

    _app.include_router(user_admin_router)
    _app.include_router(servers_router)
    _app.include_router(frontend_router)
    _app.include_router(clients_router)

    _app.mount("/static", StaticFiles(directory="src/frontend/public/static"), "static")

    _app.add_middleware(NotFoundRedirectMiddleware)

    return _app


app = get_application()
