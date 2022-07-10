from peewee import Model, AutoField, CharField

from db import db_obj


class lattesDocenteDB(Model):
    id = AutoField()
    nome = CharField()
    lattes = CharField()

    class Meta:
        database = db_obj
        schema = 'lattesDocente'
