from fastapi import APIRouter
from fastapi.responses import Response

from src.users.schemas import UserLogin,ReCreatePassword
from src.users.auth import *
from src.exceptions import IncorrectLoginOrPasswordException


router = APIRouter(
    prefix="/users",
    tags=["auth users endpoint"]
)

@router.post("/login")
async def user_login(
    response: Response, 
    user_data: UserLogin
):
    user = await authenticate_user(
        user_data.login, 
        user_data.password
    )
    if not user:
        raise IncorrectLoginOrPasswordException
    
    access_token = create_access_token({
        "sub": str(user.id)
    })

    response.set_cookie(
        "savebit_access_token",
        str(access_token),
        httponly=True
    )

@router.post('/recreatepass')
async def recreate_password(
    response: Response,
    user_recrete_data: ReCreatePassword
):
    user = await authenticate_user(
        user_recrete_data.login,
        user_recrete_data.password
    )
    if not user:
        raise IncorrectLoginOrPasswordException
    
    hashed_password = get_password_hash(user_recrete_data.newpassword)

    await UserService.update({
        "login": user_recrete_data.login
    },
    hashed_password=hashed_password
    )
    response.delete_cookie("savebit_access_token")
    return {"status": "Password changed successfully!"}
    
    




