from typing import List, Dict

from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from autenticacao import autenticacao_rotas
from autenticacao.autenticacao import usuario_jwt
from config import Settings
from db import DisciplinaDb, CursoDb
from db import ProfessorDb
from db import TurmaDb
from mensageria import mensageria
from modelos import Professor, Horario, GrupoTelegram, Curso
from modelos import Turma

settings = Settings()
app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins='*',
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(autenticacao_rotas.router)
app.include_router(mensageria.router)


@app.get('/teste')
def teste(current_user: str = Depends(usuario_jwt)):
    print(current_user)
    return {'teste': 'jwt'}


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


@app.get('/listar_emails_professores', response_model=List[Professor])
def listarEmailsProfessores():
    professores_db = ProfessorDb().select()

    professores = [Professor(ref_id=professor_db.ref_id,
                             nome=professor_db.nome,
                             email=professor_db.email) for professor_db in professores_db]

    return professores


@app.get('/listar_horarios_por_periodo', response_model=Dict[str, List[Horario]])
def listarHorariosPorPeriodo():
    turmas_db = TurmaDb().select()

    horarios = {periodo: [] for periodo in range(1, 9)}
    for turma_db in turmas_db:
        disciplina_db = DisciplinaDb().select().where(DisciplinaDb.ref_id == turma_db.disciplina_ref_id).first()
        professor_db = ProfessorDb().select().where(ProfessorDb.ref_id == turma_db.professor_ref_id).first()
        horarios[disciplina_db.periodo].append(Horario(disciplina_nome=disciplina_db.nome,
                                                       turma=turma_db.turma,
                                                       sala=turma_db.sala,
                                                       bloco=turma_db.sala,
                                                       horario=turma_db.horario,
                                                       periodo=disciplina_db.periodo,
                                                       professor_nome=professor_db.nome))

    return horarios


@app.get('/listar_grupos_telegram_por_periodo', response_model=Dict[str, List[GrupoTelegram]])
def listarGruposTelegramPorPeriodo():
    disciplinas_db = DisciplinaDb().select()

    grupos = {periodo: [] for periodo in range(1, 9)}
    for disciplina_db in disciplinas_db:
        grupos[disciplina_db.periodo].append(GrupoTelegram(nome=disciplina_db.nome,
                                                           link=disciplina_db.grupo_telegram_link))

    return grupos

@app.get('/buscar_curso/{ref_id}', response_model=Curso)
def buscarCurso(ref_id: int):
    """
    Retorna o refId e nome do Curso
    """

    curso_db = CursoDb().select().where(CursoDb.ref_id == ref_id).first()

    curso = Curso(ref_id=curso_db.ref_id,
                  nome=curso_db.nome)
    return curso
