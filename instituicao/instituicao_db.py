from peewee import Model, AutoField, CharField

from db import db_obj


class InstituicaoDB(Model):
    id = AutoField()
    nome = CharField()

    class Meta:
        database = db_obj
        schema = "instituicao"