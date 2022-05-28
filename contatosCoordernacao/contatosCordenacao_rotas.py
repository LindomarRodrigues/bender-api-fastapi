import email
import imp
from os import stat
from typing import List
import jwt
from config import Settings
from fastapi import APIRouter, Body

from contatosCoordernacao.contatosCordenacao_db import ContatosCoordenacaoDB
from contatosCoordernacao.contatosCordenacao_modelos import ContatosPostCoordenacaoModelo
from contatosCoordernacao.contatosCordenacao_modelos import ContatosGetCoordenacaoModelo
from usuario.usuario_db import TipoUsuarioDB

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
def coordenacao(enc_jwt: str, response: dict = Body(...)):
    usuario_payload = jwt.decode(enc_jwt, key=settings.jwt_secret, algorithms=["HS256"])
    
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == usuario_payload['id']).first()

    if tipo_usuario_db.tipo < 2:
        return ContatosPostCoordenacaoModelo(status= False, error="Usuario não autenticado")
    contatos_db = ContatosCoordenacaoDB().select().where((ContatosCoordenacaoDB.email == response['email'])&(ContatosCoordenacaoDB.telefone == response['telefone']))

    if contatos_db.exists():
        return ContatosPostCoordenacaoModelo(id = contatos_db.first().id, status = False)
    id_temp = ContatosCoordenacaoDB().insert(email = response['email'], telefone = response['telefone']).execute()
    return ContatosPostCoordenacaoModelo(id = id_temp, status= True)
