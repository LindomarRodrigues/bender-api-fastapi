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
    receptor_id: int


class MensagemModelo(BaseModel):
    id: int
    conteudo: str
    conversa_id: int
    responsavel: int
