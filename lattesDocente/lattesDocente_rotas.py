import email
import imp
from os import stat
from typing import List
from config import Settings
import jwt
from fastapi import APIRouter, Body

from lattesDocente.lattesDocente_db import lattesDocenteDB
from lattesDocente.lattesDocente_modelos import LattesGetDocenteModelo
from lattesDocente.lattesDocente_modelos import LattesPostDocenteModelo

from usuario.usuario_db import TipoUsuarioDB

router = APIRouter(prefix="/lattesDocente",
                   tags=["Lattes dos Docentes"])
settings = Settings()

@router.get('/lattesDocente', response_model=List[LattesGetDocenteModelo])
def latte(enc_jwt: str):
    usuario_payload = jwt.decode(enc_jwt, key=settings.jwt_secret, algorithms=["HS256"])

    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == usuario_payload['id']).first()
    
    if tipo_usuario_db.tipo < 2:
        return[ LattesPostDocenteModelo(status= False, error="Usuario não autenticado")]

    lattes = lattesDocenteDB().select()
    lattes_modelo = []
    for contato in lattes:
        lattes_modelo.append(LattesGetDocenteModelo(id= contato.id, nome= contato.nome, lattes= contato.lattes))
    return lattes_modelo

