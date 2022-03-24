from typing import List

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db import DisciplinaDb
from db import ProfessorDb
from db import TurmaDb
from modelos import Professor
from modelos import Turma

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins='*',
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get('/buscar_professor/{ref_id}', response_model=Professor)
def buscarProfessor(ref_id: int):
    """
    Retorna o refId, nome e email do professor
    """

    professor_db = ProfessorDb().select().where(ProfessorDb.ref_id == ref_id).first()

    professor = Professor(ref_id=professor_db.ref_id,
                          nome=professor_db.nome,
                          email=professor_db.email)
    return professor


@app.get('/listar_emails_professor', response_model=List[Professor])
def listarEmailsProfessor():
    professores_db = ProfessorDb().select()

    professores = [Professor(ref_id=professor_db.ref_id,
                             nome=professor_db.nome,
                             email=professor_db.email) for professor_db in professores_db]

    return professores


@app.get('/buscar_turma/{ref_id}', response_model=Turma)
def buscarTurma(ref_id: int):
    turma_db = TurmaDb().select().where(TurmaDb.ref_id == ref_id).first()

    disciplina_db = DisciplinaDb().select().where(DisciplinaDb.ref_id == turma_db.disciplina_ref_id).first()

    professor_db = ProfessorDb().select().where(ProfessorDb.ref_id == turma_db.professor_ref_id).first()

    turma = Turma(ref_id=turma_db.ref_id,
                  disciplina_nome=disciplina_db.nome,
                  semestre=turma_db.semestre,
                  ano=turma_db.ano,
                  turma=turma_db.turma,
                  sala=turma_db.sala,
                  bloco=turma_db.bloco,
                  tipo=turma_db.tipo,
                  professor_nome=professor_db.nome,
                  professor_email=professor_db.email)

    return turma
