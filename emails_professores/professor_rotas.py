import email
from os import stat
import shutil
from typing import List
from config import Settings
from fastapi import APIRouter, Body

import jwt
from autenticacao.autenticacao import usuario_jwt
from usuario.usuario_db import UsuarioDb
from fastapi import APIRouter, Depends

from emails_professores.professor_db import ContatoProfessorDB
from emails_professores.professor_modelos import ContatoPostProfessorModelo
from emails_professores.professor_modelos import ContatoGetProfessorModelo

router = APIRouter(prefix="/professores",   
                   tags=["Professores"]) 
settings = Settings()

@router.post('/professores', response_model=ContatoPostProfessorModelo)
def professores(payload: dict = Body(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    print(payload)
    # import ipdb; ipdb.set_trace()
    professor_db = ContatoProfessorDB().select().where((ContatoProfessorDB.nome == payload['nome'])&(ContatoProfessorDB.email == payload['email']))
    if professor_db.exists():
        return ContatoPostProfessorModelo(id = professor_db.first().id, status=False)
    id_temp = ContatoProfessorDB().insert(nome = payload['nome'], email=payload['email'], curso_id = current_user.curso).execute()
    return ContatoPostProfessorModelo(id = id_temp, status=True)

@router.get('/professores', response_model=List[ContatoGetProfessorModelo])
def professores(current_user: UsuarioDb = Depends(usuario_jwt)):
    profs = ContatoProfessorDB().select().where((ContatoProfessorDB.curso_id == current_user.curso))
    professor_modelo = []
    for prof in profs:
        professor_modelo.append(ContatoGetProfessorModelo(id = prof.id, curso_id=prof.curso_id ,nome = prof.nome, email = prof.email))
    return professor_modelo