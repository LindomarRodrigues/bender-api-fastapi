from pydantic import BaseModel

class LattesPostDocenteModelo(BaseModel):
    id: int
    status: bool

class LattesGetDocenteModelo(BaseModel):
    id: int
    nome: str
    lattes: str