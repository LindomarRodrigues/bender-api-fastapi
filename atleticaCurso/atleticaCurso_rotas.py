from typing import List

from fastapi import APIRouter, Depends
from fastapi import Body

from atleticaCurso.atleticaCurso_db import AtleticaCursoDB
from atleticaCurso.atleticaCurso_modelos import AtleticaCursoPostModelo, AtleticaGetCursoModelo
from autenticacao.autenticacao import usuario_jwt
from config import Settings
from usuario.usuario_db import UsuarioDb, TipoUsuarioDB

router = APIRouter(prefix="/atletica",
                   tags=["Atletica"])
settings = Settings()


# JWT do usuario (colocar)
@router.post('/atletica', response_model=AtleticaCursoPostModelo)
def Atletica(response: dict = Body(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()

    if tipo_usuario_db.tipo != 2:
        return AtleticaCursoPostModelo(status=False, error="Usuario não autenticado")
    atletica_db = AtleticaCursoDB().select().where(
        (AtleticaCursoDB.nome == response['nome']) &
        (AtleticaCursoDB.email == response['email']) &
        (AtleticaCursoDB.instagram == response['instagram']) &
        (AtleticaCursoDB.telefone == response['telefone']))
    if atletica_db.exists():
        return AtleticaCursoPostModelo(erro="Essa atletica já foi adicionada, tente novamente!", status=False)
    id_temp = AtleticaCursoDB().insert(curso_id=response['curso_id'], nome=response['nome'], email=response['email'],
                                       instagram=response['instagram'], telefone=response['telefone']).execute()
    return AtleticaCursoPostModelo(id=id_temp, status=True)


@router.get('/listar_atletica', response_model=List[AtleticaGetCursoModelo])
def Atletica(current_user: UsuarioDb = Depends(usuario_jwt)):
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()

    if tipo_usuario_db.tipo != 2:
        return [AtleticaCursoPostModelo(status=False, error="Usuario não autenticado")]

    atleticas = AtleticaCursoDB().select().where()
    atleticaCurso_modelo = []
    for atletica in atleticas:
        atleticaCurso_modelo.append(AtleticaGetCursoModelo(
            id=atletica.id,
            curso_id=atletica.curso_id,
            nome=atletica.nome,
            email=atletica.email,
            instagram=atletica.instagram,
            telefone=atletica.telefone))
    return atleticaCurso_modelo
