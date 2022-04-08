from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str
    db_nome: str
    db_usuario: str
    db_senha: str
    db_host: str
    db_porta: int

    class Config:
        env_file = ".env"
        # APP_NAME = "BenderAPI"
        # DB_NOME = "bender"
        # DB_USUARIO = ""
        # DB_SENHA = ""
        # DB_HOST = ""
        # DB_PORTA =
