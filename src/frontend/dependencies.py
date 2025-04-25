from fastapi import Request, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from datetime import datetime

from src.config import settings
from src.users.service import UserService
from src.users.models import Users


def get_token(request: Request) -> str:
    token = request.cookies.get("savebit_access_token", None)
    if not token:
        return {"detail": 'Unauthorized'}
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        if token["detail"] == "Unauthorized":
            return None
    except:
        pass
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALG      
        )
    except JWTError:
        return None
    
    expire = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        return None
    
    user_id: str = payload.get("sub")

    if not user_id:
        return None
    
    user = await UserService.find_by_id(int(user_id))
     
    if not user:
        return None

    return user

def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

    

async def get_current_admin_user(user: Users = Depends(get_current_user)):
    return user