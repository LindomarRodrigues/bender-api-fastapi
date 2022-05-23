from typing import List
from config import Settings
from fastapi import APIRouter, Body

from curso.curso_db import CursoDB
from curso.curso_modelos import CursoModeloGet
from curso.curso_modelos import CursoModeloPost

router = APIRouter(prefix="/curso",
                   tags=["curso"])

settings = Settings()


@router.get('/', response_model=List[CursoModeloGet])
def cursos():
    cursos = CursoDB().select()
    curso_modelo = []
    for curso in cursos:
        curso_modelo.append(CursoModeloGet(id=curso.id, nome=curso.nome, campus_id=curso.campus_id.id))
    return curso_modelo


@router.post('/novo', response_model=CursoModeloPost)
def cursos(nome: str, campusid: int):
    cursos_db = CursoDB().select().where((CursoDB.nome == nome) & (CursoDB.campus_id == campusid))

    if cursos_db.exists():
        return CursoModeloPost(id=cursos_db.first().id, status=False)
    id_temp = CursoDB().insert(nome=nome, campus_id=campusid).execute()
    return CursoModeloPost(id=id_temp, status=True)
