from pydantic import BaseModel
from typing import Optional

class AtualizarInstagram(BaseModel):
    id: Optional[int]
    status: bool
    error: Optional[str]

class InstagramModeloGet(BaseModel):
    id: Optional[int]
    nome_do_perfil: Optional[str]
    link: Optional[str]
    error: Optional[str]
