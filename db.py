from peewee import SqliteDatabase, Model, IntegerField, CharField

db_obj = SqliteDatabase('db.db')


class ProfessorDb(Model):
    ref_id = IntegerField(primary_key=True)
    nome = CharField()
    email = CharField()

    class Meta:
        database = db_obj


class DisciplinaDb(Model):
    ref_id = IntegerField(primary_key=True)
    nome = CharField()

    class Meta:
        database = db_obj


class TurmaDb(Model):
    ref_id = IntegerField(primary_key=True)
    disciplina_ref_id = IntegerField()
    semestre = CharField()
    ano = IntegerField()
    turma = CharField()
    sala = CharField()
    bloco = CharField()
    tipo = CharField()  # Hibrido/Remoto/Presencial
    professor_ref_id = IntegerField()

    class Meta:
        database = db_obj


db_obj.create_tables([DisciplinaDb, TurmaDb])
