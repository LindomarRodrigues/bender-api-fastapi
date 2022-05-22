from asyncio.windows_events import NULL
from pydantic import BaseModel
from typing import Optional

class AtleticaCursoPostModelo(BaseModel):
    erro: Optional [str] = NULL
    status: bool

class AtleticaGetCursoModelo(BaseModel):
    id: int
    curso_id: int
    nome: str
    email: str
    instagram: str
    telefone: str

# class AtleticaPostCursoModelo(BaseModel):
#     nome: str
#     email: str
#     instagram: str
#     telefone: str