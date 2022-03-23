from pydantic import BaseModel


class Professor(BaseModel):
    ref_id: int
    nome: str
    email: str
