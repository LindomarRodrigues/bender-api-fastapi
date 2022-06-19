from typing import List

import jwt
from fastapi import APIRouter, Body
from urllib3 import Retry
from config import Settings

import jwt
from autenticacao.autenticacao import usuario_jwt
from usuario.usuario_db import UsuarioDb, TipoUsuarioDB
from fastapi import APIRouter, Depends

from instagram.instagram_db import InstagramDB
from instagram.instagram_modelos import AtualizarInstagram, InstagramModeloGet
from usuario.usuario_db import TipoUsuarioDB

router = APIRouter(prefix="/instagram",
                   tags=["Instagram"])
settings = Settings()


@router.post('/adicionar_instagram', response_model = AtualizarInstagram)
def adicionar_instagram(response: dict = Body(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()

    if tipo_usuario_db.tipo != 2:
        return AtualizarInstagram(erro = 'Usuario não autenticado', status=False)
    instagram_db = InstagramDB().select().where((
        InstagramDB.nome_do_perfil  == response['nome_do_perfil'])&
        (InstagramDB.link == response['link']))
    if instagram_db.exists():
        return AtualizarInstagram(error = "Esta conta já foi adicionada", status=False)
    id_instagram = InstagramDB.insert(nome_do_perfil = response['nome_do_perfil'], link = response['link']).execute()
    return AtualizarInstagram(id=id_instagram, status=True)

@router.get('/listar_instagrams', response_model=List[InstagramModeloGet])
def listar_instagrams(current_user: UsuarioDb = Depends(usuario_jwt)):

    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return [AtualizarInstagram(status= False, error="Usuario não autenticado")]

    instagrams = InstagramDB().select()
    list_instagram = []
    for instagram in instagrams:
       list_instagram.append(InstagramModeloGet(
        id= instagram.id, 
        nome_do_perfil= instagram.nome_do_perfil,
        link= instagram.link))
    return list_instagram
