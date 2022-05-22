from os import stat
from typing import List
from config import Settings
from fastapi import APIRouter, Body

from atleticaCurso.atleticaCurso_db import AtleticaCursoDB
from atleticaCurso.atleticaCurso_modelos import AtleticaCursoPostModelo, AtleticaGetCursoModelo

router = APIRouter(prefix="/atletica",
                   tags=["Atletica"])
settings = Settings()

@router.post('/atletica', response_model=AtleticaCursoPostModelo)
def Atletica(response: dict = Body(...)):
    print(response)
    atleticaCurso_db = AtleticaCursoDB().select().where((AtleticaCursoDB.nome == response['nome'])&(AtleticaCursoDB.email == response['email']))
    if atleticaCurso_db.exists():
        return AtleticaCursoPostModelo(erro="Essa atletica já foi adicionada, tente novamente!", status=False)
    id_temp = AtleticaCursoDB().insert(curso_id = response['curso_id'], nome = response['nome'], email=response['email'], instagram=response['instagram'], telefone=response['telefone']).execute()
    return AtleticaCursoPostModelo(status=True)

@router.get('/listar_atletica', response_model=List[AtleticaGetCursoModelo])
def Atletica():
    atleticas = AtleticaCursoDB().select()
    atleticaCurso_modelo = []
    for atletica in atleticas:
        atleticaCurso_modelo.append(AtleticaGetCursoModelo(id = atletica.id, curso_id = atletica.curso_id, nome = atletica.nome, email = atletica.email, instagram = atletica.instagram, telefone = atletica.telefone))
    return atleticaCurso_modelo