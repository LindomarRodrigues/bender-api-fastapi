from pydantic import BaseModel
from typing import Optional

class InformesPostModelo(BaseModel):
    id: Optional[int]
    error: Optional[str]
    status: bool
    

class InformesGetModelo(BaseModel):
    id: int
    curso_id: int
    remetente: str
    aviso: str
    link: str