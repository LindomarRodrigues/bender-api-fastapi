from pydantic import BaseModel


class CursoModeloGet(BaseModel):
    id: int
    nome: str
    campus_id: int


class CursoModeloPost(BaseModel):
    id: int
    status: bool
