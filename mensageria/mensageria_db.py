from peewee import Model, CharField, AutoField, ForeignKeyField, IntegerField, DateTimeField

from usuario.usuario_db import Usuario
from db import db_obj


class Conversa(Model):
    id = AutoField()
    autor_id = ForeignKeyField(Usuario, backref='conversas_iniciadas')
    receptor_id = ForeignKeyField(Usuario, backref='conversas_convidadas')

    class Meta:
        database = db_obj
        schema = 'mensageria'


class Mensagem(Model):
    id = AutoField()
    conteudo = CharField(max_length=1024)
    conversa_id = ForeignKeyField(Conversa, backref='mensagens')
    responsavel = IntegerField()  # 1 --> autor | 2 --> receptor

    class Meta:
        database = db_obj
        schema = 'mensageria'


class MensagemStatus(Model):
    id = AutoField()
    mensagem_id = ForeignKeyField(Mensagem, backref='status')
    status = IntegerField()  # 0 --> Enviado, 1 --> Recebido, 2 --> Lido
    aconteceu_em = DateTimeField()

    class Meta:
        database = db_obj
        schema = 'mensageria'
