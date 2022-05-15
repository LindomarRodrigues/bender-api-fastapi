from typing import Optional

from pydantic import BaseModel


class FileModelo(BaseModel):
    arquivo: str
    id: int