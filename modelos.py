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
    disciplina_nome: str
    semestre: str
    ano: str
    turma: str
    sala: str
    bloco: str
    tipo: str
    professor_nome: str
    professor_email: str
