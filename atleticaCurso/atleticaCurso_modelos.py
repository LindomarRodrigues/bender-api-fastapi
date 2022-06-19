# from asyncio.windows_events import NULL
from turtle import st
from pydantic import BaseModel
from typing import Optional

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
