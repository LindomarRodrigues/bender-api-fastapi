from pydantic import BaseModel

class ContatoPostProfessorModelo(BaseModel):
    id: int
    status: bool

class ContatoGetProfessorModelo(BaseModel):
    id: int
    nome: str
    email: str