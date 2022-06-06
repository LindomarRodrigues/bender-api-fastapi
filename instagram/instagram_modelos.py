from pydantic import BaseModel
from typing import Optional

class AtualizarInstagram(BaseModel):
    id: Optional[int] = None
    erro: Optional[str] = None
    status: bool

class InstagramModeloGet(BaseModel):
    id: int
    nome_do_perfil: str
    link: str
