from pydantic import BaseModel


class InstituicaoModelo(BaseModel):
    id: int
    status: bool
