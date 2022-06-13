from typing import Optional
from pydantic import BaseModel

class RegimentoModeloPost(BaseModel):
    id: int
    status: bool

class RegimentoModeloGet(BaseModel):
    id: int
    periodo: int
    disciplina: str
    horario: str
    error: Optional[str]