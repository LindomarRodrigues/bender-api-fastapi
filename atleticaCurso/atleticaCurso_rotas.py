from os import stat
from typing import List
from config import Settings
from fastapi import APIRouter, Body
import jwt

from atleticaCurso.atleticaCurso_db import AtleticaCursoDB
from atleticaCurso.atleticaCurso_modelos import AtleticaCursoPostModelo, AtleticaGetCursoModelo
from usuario.usuario_db import TipoUsuarioDB

router = APIRouter(prefix="/atletica",
                   tags=["Atletica"])
settings = Settings()

# JWT do usuario (colocar)
@router.post('/atletica', response_model=AtleticaCursoPostModelo)
def Atletica(enc_jwt:str, nome:str, email:str, instagram:str, telefone:str, curso_id:int):
    usuario_payload = jwt.decode(enc_jwt, key=settings.jwt_secret, algorithms=["HS256"])
    
    atleticaCurso_db = AtleticaCursoDB().select().where((AtleticaCursoDB.nome == nome)&(AtleticaCursoDB.email == email))
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == usuario_payload['id']).first()

    if tipo_usuario_db.tipo < 2:
        return AtleticaCursoPostModelo(status= False, error="Usuario não autenticado")

    if atleticaCurso_db.exists():
        return AtleticaCursoPostModelo(erro="Essa atletica já foi adicionada, tente novamente!", status=False)
    id_temp = AtleticaCursoDB().insert(curso_id = curso_id, nome = nome, email = email, instagram = instagram, telefone = telefone).execute()
    return AtleticaCursoPostModelo(status=True)

@router.get('/listar_atletica', response_model=List[AtleticaGetCursoModelo])
def Atletica():
    atleticas = AtleticaCursoDB().select()
    atleticaCurso_modelo = []
    for atletica in atleticas:
        atleticaCurso_modelo.append(AtleticaGetCursoModelo(id = atletica.id, curso_id = atletica.curso_id, nome = atletica.nome, email = atletica.email, instagram = atletica.instagram, telefone = atletica.telefone))
    return atleticaCurso_modelo
