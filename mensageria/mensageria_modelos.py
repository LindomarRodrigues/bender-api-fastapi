import datetime
from typing import Optional

from pydantic import BaseModel


class ConversaIniciadaModelo(BaseModel):
    status: bool
    conversa_id: Optional[int] = None
    erro: Optional[str] = None


class MensagemEnviadaModelo(BaseModel):
    status: bool
    mensagem_id: Optional[int] = None
    erro: Optional[str] = None


class ConversaModelo(BaseModel):
    id: int
    autor_id: int
    autor_nome: str
    autor_cor: str
    receptor_id: int
    receptor_nome: str
    receptor_cor: str
    e_autor: bool
    ultima_mensagem_horario: datetime.datetime
    ultima_mensagem: str


class MensagemModelo(BaseModel):
    id: int
    conteudo: str
    conversa_id: int
    responsavel: int
