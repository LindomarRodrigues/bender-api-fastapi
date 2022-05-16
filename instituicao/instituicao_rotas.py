from typing import List
from config import Settings
from fastapi import APIRouter, Body

from instituicao.instituicao_db import InstituicaoDB
from instituicao.instituicao_modelos import InstituicaoModelo

router = APIRouter(prefix="/instituicao",
                   tags=["instituicao"])

settings = Settings()


@router.get('/', response_model=List[InstituicaoModelo])
def instituicao():
    instituicoes = InstituicaoDB().select()
    instituicoes_modelo = []
    for instituicao in instituicoes:
        instituicoes_modelo.append(InstituicaoModelo(id=instituicao.id, status=True))
        return instituicoes_modelo


@router.post('/novo', response_model=InstituicaoModelo)
def instituicao(response: dict = Body(...)):
    instituicoes_db = InstituicaoDB().select().where((InstituicaoDB.nome == response['nome']))

    if instituicoes_db.exists():
        return InstituicaoModelo(id=instituicoes_db.first().id, status=False)
    id_temp = InstituicaoDB().insert(nome=response['nome']).execute()
    return InstituicaoModelo(id=id_temp, status=True)
