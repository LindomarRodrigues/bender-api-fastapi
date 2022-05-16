import email
from os import stat
import shutil
from typing import List
from config import Settings
from fastapi import APIRouter, Body

from emailsprofessores.professor_db import ContatoProfessorDB
from emailsprofessores.professor_modelos import ContatoPostProfessorModelo
from emailsprofessores.professor_modelos import ContatoGetProfessorModelo

router = APIRouter(prefix="/professores",   
                   tags=["Professores"]) 
settings = Settings()

@router.post('/professores', response_model=ContatoPostProfessorModelo)
def professores(payload: dict = Body(...)):
    print(payload)
    # import ipdb; ipdb.set_trace()
    professor_db = ContatoProfessorDB().select().where((ContatoProfessorDB.nome == payload['nome'])&(ContatoProfessorDB.email == payload['email']))
    if professor_db.exists():
        return ContatoPostProfessorModelo(id = professor_db.first().id, status=False)
    id_temp = ContatoProfessorDB().insert(nome = payload['nome'], email=payload['email']).execute()
    return ContatoPostProfessorModelo(id = id_temp, status=True)

@router.get('/professores', response_model=List[ContatoGetProfessorModelo])
def professores():
    profs = ContatoProfessorDB().select()
    professor_modelo = []
    for prof in profs:
        professor_modelo.append(ContatoGetProfessorModelo(id = prof.id, nome = prof.nome, email = prof.email))
    return professor_modelo