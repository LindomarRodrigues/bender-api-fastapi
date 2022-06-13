from typing import List, Dict

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from autenticacao import autenticacao_rotas
from instagram import instagram_rotas
from autenticacao.autenticacao_db import UsuarioAuthDb, JwtRefreshTokenDb
from config import Settings
from contatos_coordernacao import contatos_coordenacao_rotas
from contatos_coordernacao.contatos_coordenacao_db import ContatosCoordenacaoDB
from db import DisciplinaDb, ProfessorDb, TurmaDb, db_obj
from emails_professores import professor_rotas
from emails_professores.professor_db import ContatoProfessorDB
from mensageria import mensageria

from atleticaCurso import atleticaCurso_rotas
from atleticaCurso.atleticaCurso_db import AtleticaCursoDB

from modelos import Professor, Horario, GrupoTelegram, Turma
from usuario import usuario_rotas
from usuario.usuario_db import TipoUsuarioDB, TurmasUsuarioDb, UsuarioDb

db_obj.create_tables(
    [TurmaDb, DisciplinaDb, ProfessorDb, ContatoProfessorDB, ContatosCoordenacaoDB, TipoUsuarioDB, TurmasUsuarioDb,
     UsuarioDb, UsuarioAuthDb, JwtRefreshTokenDb, AtleticaCursoDB])

settings = Settings()
app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=100)

app.add_middleware(CORSMiddleware,
                   allow_origins='*',
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(autenticacao_rotas.router)

app.include_router(mensageria.router)
app.include_router(usuario_rotas.router)
app.include_router(professor_rotas.router)
app.include_router(instagram_rotas.router)
app.include_router(contatos_coordenacao_rotas.router)
app.include_router(atleticaCurso_rotas.router)

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
