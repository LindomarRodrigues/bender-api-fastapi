from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str

    class Config:
        env_file = ".env"
