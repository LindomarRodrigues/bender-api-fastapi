from typing import List

import jwt
from fastapi import APIRouter
from config import Settings
from instagram.instagram_db import Instagram
from instagram.instagram_modelos import AtualizarInstagram, InstagramModeloGet
from usuario.usuario_db import TipoUsuarioDB

router = APIRouter(prefix="/instagram",
                   tags=["Instagram"])
settings = Settings()


@router.post('/adicionar_instagram', response_model = AtualizarInstagram)
def adicionar_instagram( enc_jwt: str, nome_do_perfil: str, link: str):
    usuario_payload = jwt.decode(enc_jwt, key=settings.jwt_secret, algorithms=["HS256"])
    usuario = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == usuario_payload['id']).first()
    if usuario.tipo != 2:
        return AtualizarInstagram(erro = 'Usuario não autenticado', status=False)
    instagram_db = Instagram().select().where((Instagram.link  == link))
    if instagram_db.exists():
        return AtualizarInstagram(erro = "Esta conta já foi adicionada", status=False)
    id_instagram = Instagram.insert(nome_do_perfil = nome_do_perfil, link = link).execute()
    return AtualizarInstagram(id=id_instagram, status=True)

@router.get('/listar_instagrams', response_model=List[InstagramModeloGet])
def listar_instagrams():
    list_instagram = []
    instagrams = Instagram().select()
    for instagram in instagrams:
       list_instagram.append(InstagramModeloGet(id= instagram.id, nome_do_perfil= instagram.nome_do_perfil, link= instagram.link))
    return list_instagram
