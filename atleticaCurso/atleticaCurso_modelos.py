from pydantic import BaseModel
from typing import Optional

class AtleticaCursoPostModelo(BaseModel):
    id: Optional[int]
    error: Optional[str]
    status: bool
    

class AtleticaGetCursoModelo(BaseModel):
    id: int
    curso_id: int
    nome: str
    email: str
    instagram: str
    telefone: str
