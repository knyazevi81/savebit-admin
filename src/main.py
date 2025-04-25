from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from src.database import create_tables
from src.users.service import UserService
from src.users.auth import get_password_hash
from src.config import settings
from src.users.router import router as user_admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()

    existing_user = await UserService.find_one_or_none(login=settings.PREREG_LOGIN)

    if not existing_user:
        
        hashed_password = get_password_hash(settings.PREREG_PASSWORD)
        await UserService.add(
            login=settings.PREREG_LOGIN,
            hashed_password=hashed_password
        )
    yield

def get_application() -> FastAPI:
    _app = FastAPI(
        title="Savebit admin panel API",
        lifespan=lifespan
    )

    _app.include_router(user_admin_router)

    _app.mount("/static", StaticFiles(directory="src/frontend/public/static"), "static")

    return _app

app = get_application()
