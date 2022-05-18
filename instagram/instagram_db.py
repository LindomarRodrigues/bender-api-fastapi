from peewee import Model, AutoField, CharField
from db import db_obj

class Instagram(Model):
    id = AutoField()
    nome_do_perfil = CharField()
    link = CharField()

    class Meta:
        database = db_obj
        schema = 'instagram'

db_obj.create_tables([Instagram]) 