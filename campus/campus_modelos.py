from pydantic import BaseModel


class CampusModeloGet(BaseModel):
    id: int
    nome: str
    inst_id: int

class CampusModeloPost(BaseModel):
    id: int
    status: bool
