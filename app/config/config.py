from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI auth rest"
    db_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"


def get_setting():
    return Settings()
