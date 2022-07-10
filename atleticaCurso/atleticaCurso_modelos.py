from typing import Optional

from pydantic import BaseModel


class AtleticaCursoPostModelo(BaseModel):
    id: Optional[int]
    error: Optional[str]
    status: bool


class AtleticaGetCursoModelo(BaseModel):
    id: Optional[int]
    curso_id: Optional[int]
    nome: Optional[str]
    email: Optional[str]
    instagram: Optional[str]
    telefone: Optional[str]
    error: Optional[str]

# class AtleticaPostCursoModelo(BaseModel):
#     nome: str
#     email: str
#     instagram: str
#     telefone: str
