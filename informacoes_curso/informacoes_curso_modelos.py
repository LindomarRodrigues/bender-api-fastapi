from typing import Optional

from pydantic import BaseModel


class InformacoesCursoPost(BaseModel):
    id: Optional[int]
    error: Optional[str]
    status: bool
