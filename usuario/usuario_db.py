from peewee import Model, CharField, ForeignKeyField, IntegerField, AutoField

from autenticacao.autenticacao_db import UsuarioAuthDb
from db import db_obj


class UsuarioDb(Model):
    id = ForeignKeyField(UsuarioAuthDb, backref='usuario', primary_key=True)
    instituicao = IntegerField(null=True)
    campus = IntegerField(null=True)
    curso = IntegerField(null=True)
    foto = CharField(max_length=2048, null=True)
    cor = CharField(null=True)

    class Meta:
        database = db_obj
        schema = 'usuario'
        db_table = 'usuario'


class TurmasUsuarioDb(Model):
    id = AutoField()
    turma_id = IntegerField(null=True)
    usuario_id = ForeignKeyField(UsuarioDb, backref='turmas')

    class Meta:
        database = db_obj
        schema = 'usuario'
        db_table = 'turmasusuario'


class TipoUsuarioDB(Model):
    id = AutoField()
    usuario_id = ForeignKeyField(UsuarioAuthDb, backref='tipo')
    tipo = IntegerField()  # 0 = Anonimo, 1 = Usuario comum, 2 = Adminstrador

    class Meta:
        database = db_obj
        schema = 'usuario'
        table_name = 'tipo_usuario'
