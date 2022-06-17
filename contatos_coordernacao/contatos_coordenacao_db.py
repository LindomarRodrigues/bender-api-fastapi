from peewee import Model, AutoField, CharField, IntegerField

from db import db_obj

class ContatosCoordenacaoDB(Model):
    id = AutoField()
    curso_id = IntegerField()
    email = CharField()
    telefone = CharField()

    class Meta:
        database = db_obj
        schema = 'contatosCoordenacao'