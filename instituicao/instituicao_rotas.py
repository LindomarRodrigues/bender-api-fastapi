from typing import List
from config import Settings
from fastapi import APIRouter, Body

from instituicao.instituicao_db import InstituicaoDB
from instituicao.instituicao_modelos import InstituicaoModeloGet
from instituicao.instituicao_modelos import InstituicaoModeloPost

router = APIRouter(prefix="/instituicao",
                   tags=["instituicao"])

settings = Settings()


@router.get('/', response_model=List[InstituicaoModeloGet])
def instituicaos():
    instituicoes = InstituicaoDB().select()
    instituicoes_modelo = []
    for instituicao in instituicoes:
        instituicoes_modelo.append(InstituicaoModeloGet(id=instituicao.id, nome=instituicao.nome, status=True))
    return instituicoes_modelo


@router.post('/novo', response_model=InstituicaoModeloPost)
def instituicao(nome: str):
    instituicoes_db = InstituicaoDB().select().where((InstituicaoDB.nome == nome))

    if instituicoes_db.exists():
        return InstituicaoModeloPost(id=instituicoes_db.first().id, status=False)
    id_temp = InstituicaoDB().insert(nome=nome).execute()
    return InstituicaoModeloPost(id=id_temp, status=True)
