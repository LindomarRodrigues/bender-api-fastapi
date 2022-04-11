from typing import Optional

from pydantic import BaseModel


class UsuarioModelo(BaseModel):
    nome: str
    instituicao: Optional[str]
    campus: Optional[str]
    curso: Optional[str]
    foto: Optional[str]
    cor: Optional[str]
    id: int


class AtualizarUsuarioModelo(BaseModel):
    status: bool
    erro: Optional[str]
