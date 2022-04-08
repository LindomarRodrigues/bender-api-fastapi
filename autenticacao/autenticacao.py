import datetime

import jwt
from fastapi import APIRouter, status
from playhouse.shortcuts import model_to_dict

from autenticacao.autenticacao_db import Usuario, JwtRefreshToken
from autenticacao.autenticacao_modelos import CadastroModelo, EntrarModelo, AtualizarJwtModelo
from config import Settings
from utilitarios.geral import gerar_hash_sha256, verificar_email

router = APIRouter(prefix="/autenticacao",
                   tags=["Autenticação"])
settings = Settings()


@router.post('/cadastrar', status_code=status.HTTP_201_CREATED, response_model=CadastroModelo)
def cadastrar(nome: str, email: str, senha: str):
    if len(nome) == 0:
        return CadastroModelo(status=False, erro='Nome inválido')
    elif len(senha) < 8:
        return CadastroModelo(status=False, erro='Senha muito curta')
    elif verificar_email(email) is False:
        return CadastroModelo(status=False, erro='Email inválido')
    else:
        usuario = Usuario().select().where(Usuario.email == email)
        if usuario.exists():
            return CadastroModelo(status=False, erro='Email já cadastrado')

        usuario = Usuario().select().where(Usuario.nome == nome)
        if usuario.exists():
            return CadastroModelo(status=False, erro='Nome já cadastrado')

    senha_hash = gerar_hash_sha256(senha)

    usuario = Usuario(nome=nome,
                      email=email,
                      registrado_em=datetime.datetime.now(),
                      ultimo_acesso_em=datetime.datetime.now(),
                      senha_hash=senha_hash)
    usuario.save()

    return CadastroModelo(status=True)


@router.post('/entrar', response_model=EntrarModelo)
def entrar(email: str, senha: str):
    usuario = Usuario().select().where(Usuario.email == email)
    if not usuario.exists():
        return EntrarModelo(status=False, erro='Email não cadastrado')
    usuario = usuario.first()
    senha_hash = gerar_hash_sha256(senha)
    if senha_hash != usuario.senha_hash:
        return EntrarModelo(status=False, erro='Senha incorreta')

    usuario_payload = model_to_dict(usuario)
    usuario_payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=settings.tempo_expiracao_jwt)

    usuario_payload['jwt_refresh_id'] = JwtRefreshToken.insert(emitido_em=datetime.datetime.now(),
                                                               expira_em=usuario_payload['exp'],
                                                               invalidado_em=None,
                                                               id_ultimo_token=None,
                                                               usuario_id=usuario.id).execute()

    for chave_datetime in ['registrado_em', 'ultimo_acesso_em']:
        usuario_payload[chave_datetime] = usuario_payload[chave_datetime].isoformat()

    usuario_payload['exp'] = usuario_payload['exp'].timestamp()

    enc_jwt = jwt.encode(payload=usuario_payload, key=settings.jwt_secret, algorithm='HS256')

    usuario.ultimo_acesso_em = datetime.datetime.now()
    usuario.save()
    return EntrarModelo(status=True, jwt=enc_jwt)


@router.post('/atualizar_jwt', response_model=AtualizarJwtModelo)
def atualizar_jwt(enc_jwt: str):
    usuario_payload = jwt.decode(enc_jwt, key=settings.jwt_secret, algorithms=["HS256"])

    jwt_refresh_token = JwtRefreshToken().select() \
        .where(JwtRefreshToken.id == usuario_payload['jwt_refresh_id']).first()
    jwt_refresh_token.invalidado_em = datetime.datetime.now()
    jwt_refresh_token.save()
    id_ultimo_token = usuario_payload['jwt_refresh_id']

    usuario = Usuario().select().where(Usuario.id == usuario_payload['id']).first()

    usuario_payload = model_to_dict(usuario)
    usuario_payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=settings.tempo_expiracao_jwt)

    usuario_payload['jwt_refresh_id'] = JwtRefreshToken.insert(emitido_em=datetime.datetime.now(),
                                                               expira_em=usuario_payload['exp'],
                                                               invalidado_em=None,
                                                               id_ultimo_token=id_ultimo_token,
                                                               usuario_id=usuario_payload['id']).execute()

    for chave_datetime in ['registrado_em', 'ultimo_acesso_em']:
        usuario_payload[chave_datetime] = usuario_payload[chave_datetime].isoformat()

    usuario_payload['exp'] = usuario_payload['exp'].timestamp()
    enc_jwt = jwt.encode(payload=usuario_payload, key=settings.jwt_secret, algorithm='HS256')

    usuario.ultimo_acesso_em = datetime.datetime.now()
    usuario.save()
    return AtualizarJwtModelo(status=True, jwt=enc_jwt)
