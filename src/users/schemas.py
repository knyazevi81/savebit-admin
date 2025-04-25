from pydantic import BaseModel

class UserLogin(BaseModel):
    login: str
    password: str

class ReCreatePassword(BaseModel):
    login: str
    password: str
    newpassword: str