from pydantic import BaseModel
from typing import Optional

class AtualizarInstagram(BaseModel):
    erro: Optional[str] = None
    status: bool

class InstagramModeloGet(BaseModel):
    id: int
    nome_do_perfil: str
    link: str
class InstagramModeloPost(BaseModel):
    nome_do_perfil: str
    link: str