from peewee import Model, AutoField, CharField, IntegerField

from db import db_obj


class ContatoProfessorDB(Model):
    id = AutoField()
    curso_id = IntegerField()
    nome = CharField()
    email = CharField()

    class Meta:
        database = db_obj
        schema = 'professoresContatos'
