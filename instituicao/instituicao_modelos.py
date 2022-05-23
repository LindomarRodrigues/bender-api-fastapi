from pydantic import BaseModel


class InstituicaoModeloPost(BaseModel):
    id: int
    status: bool

class InstituicaoModeloGet(BaseModel):
    id: int
    nome: str
