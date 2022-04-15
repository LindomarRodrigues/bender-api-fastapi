from peewee import Model, CharField, DateTimeField, AutoField, ForeignKeyField

from db import db_obj


class UsuarioAuth(Model):
    id = AutoField()
    nome = CharField(max_length=150)
    email = CharField(max_length=150)
    registrado_em = DateTimeField()
    ultimo_acesso_em = DateTimeField(null=True)
    senha_hash = CharField(max_length=64)

    class Meta:
        database = db_obj
        schema = 'autenticacao'


class JwtRefreshToken(Model):
    id = AutoField()
    emitido_em = DateTimeField()
    expira_em = DateTimeField()
    invalidado_em = DateTimeField(null=True)
    id_ultimo_token = ForeignKeyField('self', backref='proximo_token', null=True)
    usuario_id = ForeignKeyField(UsuarioAuth, backref='jwt_tokens')

    class Meta:
        database = db_obj
        schema = 'autenticacao'
