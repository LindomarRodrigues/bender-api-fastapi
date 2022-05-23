from peewee import Model, AutoField, CharField, ForeignKeyField

from db import db_obj
from instituicao.instituicao_db import InstituicaoDB


class CampusDB(Model):
    id = AutoField()
    nome = CharField()
    inst_id = ForeignKeyField(InstituicaoDB, backref="campus")

    class Meta:
        database = db_obj
        schema = "campus"