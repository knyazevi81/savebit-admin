from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    ALG: str
    PREREG_LOGIN: str
    PREREG_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings() # type: ignore
