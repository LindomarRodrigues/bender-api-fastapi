from peewee import Model, IntegerField, CharField, PostgresqlDatabase, AutoField, ForeignKeyField
from playhouse.shortcuts import ReconnectMixin

from config import Settings


class ReconnectPostgresqlDatabase(ReconnectMixin, PostgresqlDatabase):
    pass


settings = Settings()
db_obj = ReconnectPostgresqlDatabase(settings.db_nome, user=settings.db_usuario, password=settings.db_senha,
                                     host=settings.db_host, port=settings.db_porta)


class ProfessorDb(Model):
    ref_id = AutoField()
    nome = CharField()
    email = CharField()

    class Meta:
        database = db_obj
        schema = 'dados_estaticos'


class DisciplinaDb(Model):
    ref_id = AutoField()
    nome = CharField()
    periodo = IntegerField(null=True)
    grupo_telegram_link = CharField(null=True)

    class Meta:
        database = db_obj
        schema = 'dados_estaticos'


class TurmaDb(Model):
    ref_id = AutoField()
    disciplina_ref_id = ForeignKeyField(DisciplinaDb, backref='turmas')
    semestre = CharField()
    ano = IntegerField()
    turma = CharField()
    sala = CharField()
    bloco = CharField()
    horario = CharField()
    tipo = CharField()  # Hibrido/Remoto/Presencial
    professor_ref_id = ForeignKeyField(ProfessorDb, backref='turmas', null=True)

    class Meta:
        database = db_obj
        schema = 'dados_estaticos'


# db_obj.drop_tables([TurmaDb, DisciplinaDb, ProfessorDb])
# db_obj.create_tables([TurmaDb, DisciplinaDb, ProfessorDb])
