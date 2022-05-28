from typing import Optional
from pydantic import BaseModel

class ContatosPostCoordenacaoModelo(BaseModel):
    id: Optional[int]
    status: bool
    error: Optional[str]

class ContatosGetCoordenacaoModelo(BaseModel):
    id: int
    email: str
    telefone: str