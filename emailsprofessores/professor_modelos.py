from pydantic import BaseModel

class ContatoProfessorModelo(BaseModel):
    id: int
    status: bool