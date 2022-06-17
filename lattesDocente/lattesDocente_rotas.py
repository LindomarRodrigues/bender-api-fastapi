import email
import imp
from os import stat
from typing import List
from config import Settings
import jwt
from fastapi import APIRouter, Body

import jwt
from autenticacao.autenticacao import usuario_jwt
from usuario.usuario_db import UsuarioDb, TipoUsuarioDB
from fastapi import APIRouter, Depends


from lattesDocente.lattesDocente_db import lattesDocenteDB
from lattesDocente.lattesDocente_modelos import LattesGetDocenteModelo
from lattesDocente.lattesDocente_modelos import LattesPostDocenteModelo

from usuario.usuario_db import TipoUsuarioDB

router = APIRouter(prefix="/lattesDocente",
                   tags=["Lattes dos Docentes"])
settings = Settings()

@router.get('/lattesDocente', response_model=List[LattesGetDocenteModelo])
def latte(current_user: UsuarioDb = Depends(usuario_jwt)):

    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    
    if tipo_usuario_db.tipo < 2:
        return[ LattesPostDocenteModelo(status= False, error="Usuario não autenticado")]

    lattes = lattesDocenteDB().select()
    lattes_modelo = []
    for contato in lattes:
        lattes_modelo.append(LattesGetDocenteModelo(id= contato.id, nome= contato.nome, lattes= contato.lattes))
    return lattes_modelo

