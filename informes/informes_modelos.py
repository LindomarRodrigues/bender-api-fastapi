from typing import Optional

from pydantic import BaseModel


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
