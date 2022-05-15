from peewee import Model, IntegerField, AutoField, CharField

from db import db_obj

class ContatoProfessorDB(Model):
    id = AutoField()
    nome = CharField()
    email = CharField()

    class Meta:
        database = db_obj
        schema = 'professoresContatos'