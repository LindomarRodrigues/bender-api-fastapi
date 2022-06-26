
from peewee import Model, CharField, AutoField, BlobField

from db import db_obj


class InformacoesCursoDB(Model):
    id = AutoField()
    pdf_name = CharField(null=True)
    pdf = BlobField()

    class Meta:
        database = db_obj
        schema = 'informacoesCurso'
        table_name = 'informacoes_curso'