from peewee import Model, AutoField, CharField, IntegerField

from db import db_obj


class RegimentoDB(Model):
    id = AutoField()
    periodo = IntegerField()
    disciplina = CharField()
    horario = CharField()

    class Meta:
        database = db_obj
        schema = 'regimento'
