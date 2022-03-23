from pydantic import BaseModel


class Professor(BaseModel):
    ref_id: int
    nome: str
    email: str


class Disciplina(BaseModel):
    ref_id: int
    nome: str


class Turma(BaseModel):
    ref_id: int
    disciplina_ref_id: int
    semestre: str
    ano: str
    turma: str
    sala: str
    bloco: str
    tipo: str
    professor_ref_id: int
