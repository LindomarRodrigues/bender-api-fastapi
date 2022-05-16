import email
import imp
from os import stat
from typing import List
from config import Settings
from fastapi import APIRouter, Body

from contatosCoordernacao.contatosCordenacao_db import ContatosCoordenacaoDB
from contatosCoordernacao.contatosCordenacao_modelos import ContatosPostCoordenacaoModelo
from contatosCoordernacao.contatosCordenacao_modelos import ContatosGetCoordenacaoModelo

router = APIRouter(prefix="/contatosCoordenacao",
                   tags=["Contatos Coordenacao"])
settings = Settings()

@router.get('/contatosCoordenacao', response_model=List[ContatosGetCoordenacaoModelo])
def coordenacao():
    contatos = ContatosCoordenacaoDB().select()
    contatos_modelo = []
    for contato in contatos:
        contatos_modelo.append(ContatosGetCoordenacaoModelo(id= contato.id, email= contato.email, telefone= contato.telefone))
    return contatos_modelo

@router.post('contatosCoordenacao/', response_model=ContatosPostCoordenacaoModelo)
def coordenacao(response: dict = Body(...)):
    print(response)
    contatos_db = ContatosCoordenacaoDB().select().where((ContatosCoordenacaoDB.email == response['email'])&(ContatosCoordenacaoDB.telefone == response['telefone']))

    if contatos_db.exists():
        return ContatosPostCoordenacaoModelo(id = contatos_db.first().id, status = False)
    id_temp = ContatosCoordenacaoDB().insert(email = response['email'], telefone = response['telefone']).execute()
    return ContatosPostCoordenacaoModelo(id = id_temp, status= True)
