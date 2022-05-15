from peewee import Model, IntegerField, AutoField, CharField

from db import db_obj

class File(Model):
    id = AutoField()
    arquivo = CharField()

    class Meta:
        database = db_obj
        schema = 'files'