from fastapi import HTTPException, status


class UserException(HTTPException):
    status_code: status = status.HTTP_401_UNAUTHORIZED
    detail: str = "Base user exception"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class JWTException(HTTPException):
    status_code: status = status.HTTP_401_UNAUTHORIZED
    detail: str = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserAlreadyExist(UserException):
    status_code: str = status.HTTP_400_BAD_REQUEST
    detail: str = "User already exist"

class IncorrectLoginOrPasswordException(UserException):
    status_code: status

class TokenExpireException(JWTException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен истек"


class TokenAbsentException(JWTException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Токен отсутствует"


class IncorrectTokenFormatException(JWTException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Неверный формат токена"


class UserIsNotPresentException(JWTException):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="none"