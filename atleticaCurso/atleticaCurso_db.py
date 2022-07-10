from peewee import Model, AutoField, CharField, IntegerField

from db import db_obj


class AtleticaCursoDB(Model):
    id = AutoField()
    curso_id = IntegerField()
    nome = CharField()
    email = CharField()
    instagram = CharField()
    telefone = CharField()

    class Meta:
        database = db_obj
        schema = 'atleticaCurso'
