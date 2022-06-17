from typing import List

import jwt
from fastapi import APIRouter, Body, Depends

from autenticacao.autenticacao import usuario_jwt
from usuario.usuario_db import UsuarioDb

from config import Settings
from contatos_coordernacao.contatos_coordenacao_db import ContatosCoordenacaoDB
from contatos_coordernacao.contatos_coordenacao_modelos import ContatosGetCoordenacaoModelo, \
    ContatosPostCoordenacaoModelo
from usuario.usuario_db import TipoUsuarioDB

router = APIRouter(prefix="/contatosCoordenacao",
                   tags=["Contatos Coordenacao"])
settings = Settings()


@router.get('/contatosCoordenacao', response_model=List[ContatosGetCoordenacaoModelo])
def coordenacao(current_user: UsuarioDb = Depends(usuario_jwt)):

    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()

    if tipo_usuario_db.tipo != 2:
        return [ContatosPostCoordenacaoModelo(status= False, error="Usuario não autenticado")]
        
    contatos = ContatosCoordenacaoDB().select().where(ContatosCoordenacaoDB.curso_id == current_user.curso)
    contatos_modelo = []
    for contato in contatos:
        contatos_modelo.append(
            ContatosGetCoordenacaoModelo(id=contato.id, email=contato.email, telefone=contato.telefone, curso_id=contato.curso_id))
    return contatos_modelo


@router.post('/contatosCoordenacao', response_model=ContatosPostCoordenacaoModelo)
def coordenacao(response: dict = Body(...), current_user: UsuarioDb = Depends(usuario_jwt)):

    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()

    if tipo_usuario_db.tipo < 2:
        return ContatosPostCoordenacaoModelo(status=False, error="Usuario não autenticado")
    contatos_db = ContatosCoordenacaoDB().select().where(
        (ContatosCoordenacaoDB.email == response['email']) & (ContatosCoordenacaoDB.telefone == response['telefone']))

    if contatos_db.exists():
        return ContatosPostCoordenacaoModelo(id=contatos_db.first().id, status=False)
    id_temp = ContatosCoordenacaoDB().insert(email=response['email'], telefone=response['telefone'], curso_id=current_user.curso).execute()
    return ContatosPostCoordenacaoModelo(id=id_temp, status=True)
