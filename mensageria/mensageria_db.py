from peewee import Model, CharField, AutoField, ForeignKeyField, IntegerField, DateTimeField

from db import db_obj
from usuario.usuario_db import UsuarioDb


class ConversaDb(Model):
    id = AutoField()
    autor_id = ForeignKeyField(UsuarioDb, backref='conversas_iniciadas')
    receptor_id = ForeignKeyField(UsuarioDb, backref='conversas_convidadas')

    class Meta:
        database = db_obj
        schema = 'mensageria'
        db_table = 'conversa'


class MensagemDb(Model):
    id = AutoField()
    conteudo = CharField(max_length=1024)
    conversa_id = ForeignKeyField(ConversaDb, backref='mensagens')
    responsavel = IntegerField()  # 1 --> autor | 2 --> receptor

    class Meta:
        database = db_obj
        schema = 'mensageria'
        db_table = 'mensagem'


class MensagemStatusDb(Model):
    id = AutoField()
    mensagem_id = ForeignKeyField(MensagemDb, backref='status')
    status = IntegerField()  # 0 --> Enviado, 1 --> Recebido, 2 --> Lido
    aconteceu_em = DateTimeField()

    class Meta:
        database = db_obj
        schema = 'mensageria'
        db_table = 'mensagemstatus'
