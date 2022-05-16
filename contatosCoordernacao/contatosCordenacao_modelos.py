from pydantic import BaseModel

class ContatosPostCoordenacaoModelo(BaseModel):
    id: int
    status: bool

class ContatosGetCoordenacaoModelo(BaseModel):
    id: int
    email: str
    telefone: str