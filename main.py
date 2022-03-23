from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db import ProfessorDb
from modelos import Professor

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
