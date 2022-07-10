from peewee import Model, AutoField, CharField, IntegerField

from db import db_obj


class InformesDB(Model):
    id = AutoField()
    curso_id = IntegerField()
    remetente = CharField()
    aviso = CharField()
    link = CharField()

    class Meta:
        database = db_obj
        schema = 'informes'
