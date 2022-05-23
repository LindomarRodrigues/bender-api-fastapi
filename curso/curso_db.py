from peewee import Model, AutoField, CharField, ForeignKeyField

from db import db_obj
from campus.campus_db import CampusDB


class CursoDB(Model):
    id = AutoField()
    nome = CharField()
    campus_id = ForeignKeyField(CampusDB, backref="curso")

    class Meta:
        database = db_obj
        schema = "curso"