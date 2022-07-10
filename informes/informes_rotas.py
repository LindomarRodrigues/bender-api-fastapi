from typing import List

from fastapi import APIRouter, Depends
from fastapi import Body

from autenticacao.autenticacao import usuario_jwt
from config import Settings
from informes.informes_db import InformesDB
from informes.informes_modelos import InformesGetModelo, InformesPostModelo
from usuario.usuario_db import UsuarioDb, TipoUsuarioDB

router = APIRouter(prefix="/informes",
                   tags=["Informes"])
settings = Settings()


@router.post('/informes', response_model=InformesPostModelo)
def Atletica(payload: dict = Body(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    informes_db = InformesDB().select().where(
        (InformesDB.remetente == payload['remetente']) & (InformesDB.aviso == payload['aviso']))
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()

    if tipo_usuario_db.tipo < 2:
        return InformesPostModelo(status=False, error="Usuario não autenticado")

    if informes_db.exists():
        return InformesPostModelo(erro="Essa atletica já foi adicionada, tente novamente!", status=False)
    id_temp = InformesDB().insert(curso_id=current_user.curso, remetente=payload['remetente'], aviso=payload['aviso'],
                                  link=payload['link']).execute()
    return InformesPostModelo(status=True)


@router.get('/listar_informes', response_model=List[InformesGetModelo])
def Atletica(current_user: UsuarioDb = Depends(usuario_jwt)):
    informes = InformesDB().select().where((InformesDB.curso_id == current_user.curso))
    informes_modelo = []
    for informe in informes:
        informes_modelo.append(InformesGetModelo(id=informe.id, curso_id=informe.curso_id, remetente=informe.remetente,
                                                 aviso=informe.aviso, link=informe.link))
    return informes_modelo
