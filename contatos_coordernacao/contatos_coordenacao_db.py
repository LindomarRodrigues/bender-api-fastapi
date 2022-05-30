from peewee import Model, AutoField, CharField

from db import db_obj

class ContatosCoordenacaoDB(Model):
    id = AutoField()
    email = CharField()
    telefone = CharField()

    class Meta:
        database = db_obj
        schema = 'contatosCoordenacao'