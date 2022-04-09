from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="autenticacao/entrar")


def usuario_jwt(token: str = Depends(oauth2_scheme)):
    print(token)
    return token
