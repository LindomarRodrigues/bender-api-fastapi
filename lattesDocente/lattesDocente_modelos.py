from typing import Optional
from pydantic import BaseModel

class LattesPostDocenteModelo(BaseModel):
    id: Optional[int]
    status: bool
    error: Optional[str]

class LattesGetDocenteModelo(BaseModel):
    id: Optional[int]
    nome: Optional[str]
    lattes: Optional[str]
    error: Optional[str]

