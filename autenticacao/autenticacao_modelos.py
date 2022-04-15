from typing import Optional

from pydantic import BaseModel


class CadastroModelo(BaseModel):
    status: bool
    erro: Optional[str] = None


class EntrarModelo(BaseModel):
    status: bool
    erro: Optional[str] = None
    jwt: Optional[str] = None


class AtualizarJwtModelo(BaseModel):
    status: bool
    erro: Optional[str] = None
    jwt: Optional[str] = None
