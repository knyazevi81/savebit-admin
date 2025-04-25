from pydantic import BaseModel, Field, HttpUrl, constr


class ServerData(BaseModel):
    hostname: str = Field(..., description="Имя хоста или IP-адрес сервера")
    server_name: str = Field(..., min_length=3, max_length=50, description="Название сервера")
    port: str = Field(..., pattern=r"^\d{2,5}$", description="Порт сервера (от 2 до 5 цифр)")
    basepath: str = Field(..., description="Базовый путь API")
    login: str = Field(..., min_length=3, max_length=50, description="Логин для авторизации")
    password: str = Field(..., min_length=6, description="Пароль для авторизации")

    class Config:
        schema_extra = {
            "example": {
                "hostname": "example.com",
                "server_name": "MyServer",
                "port": "2087",
                "basepath": "/api/v1",
                "login": "admin",
                "password": "securepassword123"
            }
        }