from os import stat
from typing import List
from config import Settings
from fastapi import APIRouter, Body

import jwt
from autenticacao.autenticacao import usuario_jwt
from fastapi import APIRouter, Depends

from informes.informes_db import InformesDB
from informes.informes_modelos import InformesGetModelo, InformesPostModelo
from usuario.usuario_db import TipoUsuarioDB
from usuario.usuario_db import UsuarioDb
from autenticacao.autenticacao_db import UsuarioAuthDb

router = APIRouter(prefix="/informes",
                   tags=["Informes"])
settings = Settings()

@router.post('/informes', response_model=InformesPostModelo)
def Atletica(enc_jwt:str, remetente:str, aviso:str, link:str, current_user: UsuarioDb = Depends(usuario_jwt)):
    usuario_payload = jwt.decode(enc_jwt, key=settings.jwt_secret, algorithms=["HS256"])

    informes_db = InformesDB().select().where((InformesDB.remetente == remetente)&(InformesDB.aviso == aviso))
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == usuario_payload['id']).first()

    if tipo_usuario_db.tipo < 2:
        return InformesPostModelo(status= False, error="Usuario não autenticado")

    if informes_db.exists():
        return InformesPostModelo(erro="Essa atletica já foi adicionada, tente novamente!", status=False)
    id_temp = InformesDB().insert(curso_id = current_user.curso, remetente = remetente, aviso = aviso, link = link).execute()
    return InformesPostModelo(status=True)

@router.get('/listar_informes', response_model=List[InformesGetModelo])
def Atletica(current_user: UsuarioDb = Depends(usuario_jwt)):
    
    informes = InformesDB().select().where((InformesDB.curso_id == current_user.curso))
    informes_modelo = []
    for informe in informes:
        informes_modelo.append(InformesGetModelo(id = informe.id, curso_id = informe.curso_id, remetente = informe.remetente, aviso = informe.aviso, link = informe.link))
    return informes_modelo