from typing import List

import jwt
from fastapi import APIRouter

from autenticacao.autenticacao import usuario_jwt
from config import Settings
from instagram.instagram_db import Instagram
from instagram.instagram_modelos import AtualizarInstagram, InstagramModeloPost,InstagramModeloGet

router = APIRouter(prefix="/instagram",
                   tags=["Instagram"])
settings = Settings()


@router.post('/adicionar_instagram', response_model = List[AtualizarInstagram])
def adicionar_instagram(response: List[InstagramModeloPost]):
    list_status = []
    for instagram in response:
        instagram_db = Instagram().select().where((Instagram.link == instagram.link))
        if instagram_db.exists():
            list_status.append(AtualizarInstagram(erro = "Esta conta já foi adicionada", status=False))
            continue 
        id_instagram = Instagram.insert(nome_do_perfil = instagram.nome_do_perfil, link = instagram.link).execute()
        list_status.append(AtualizarInstagram(status=True))
    return list_status

@router.get('/listar_instagrams', response_model=List[InstagramModeloGet])
def listar_instagrams():
    list_instagram = []
    instagrams = Instagram().select()
    for instagram in instagrams:
       list_instagram.append(InstagramModeloGet(id= instagram.id, nome_do_perfil= instagram.nome_do_perfil, link= instagram.link))
    return list_instagram
