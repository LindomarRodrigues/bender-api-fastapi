from typing import Optional

from pydantic import BaseModel


class CadastroModelo(BaseModel):
    status: bool
    erro: Optional[str]


class EntrarModelo(BaseModel):
    status: bool
    erro: Optional[str]
    jwt: Optional[str]


class AtualizarJwtModelo(BaseModel):
    status: bool
    erro: Optional[str]
    jwt: Optional[str]
