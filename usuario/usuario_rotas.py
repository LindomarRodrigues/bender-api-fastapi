from typing import Optional

from fastapi import APIRouter, Depends

from autenticacao.autenticacao import usuario_jwt
from config import Settings
from usuario.usuario_db import UsuarioDb
from usuario.usuario_modelos import UsuarioModelo, AtualizarUsuarioModelo

router = APIRouter(prefix="/usuario",
                   tags=["Usuario"])
settings = Settings()


@router.get('/usuario', response_model=UsuarioModelo)
def usuario(current_user: UsuarioDb = Depends(usuario_jwt)):
    usuario_modelo = UsuarioModelo(nome=current_user.id.nome,
                                   email=current_user.id.email,
                                   instituicao=current_user.instituicao,
                                   campus=current_user.campus,
                                   curso=current_user.curso,
                                   foto=current_user.foto,
                                   cor=current_user.cor,
                                   id=current_user.id.id)

    return usuario_modelo


@router.post('/atualizar_usuario', response_model=AtualizarUsuarioModelo)
def atualizar_usuario(current_user: UsuarioDb = Depends(usuario_jwt), novos_valores: Optional[dict] = None):
    UsuarioDb().update(novos_valores).where(UsuarioDb.id == current_user.id.id).execute()

    return AtualizarUsuarioModelo(status=True)
