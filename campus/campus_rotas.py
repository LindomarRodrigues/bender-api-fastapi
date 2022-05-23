from typing import List
from config import Settings
from fastapi import APIRouter, Body

from campus.campus_db import CampusDB
from campus.campus_modelos import CampusModeloGet
from campus.campus_modelos import CampusModeloPost

router = APIRouter(prefix="/campus",
                   tags=["campus"])

settings = Settings()


@router.get('/', response_model=List[CampusModeloGet])
def campus():
    campi = CampusDB().select()
    campi_modelo = []
    for campus in campi:
        campi_modelo.append(CampusModeloGet(id=campus.id, nome=campus.nome, inst_id=campus.inst_id.id))
    return campi_modelo


@router.post('/novo', response_model=CampusModeloPost)
def campus(nome: str, instid: int):
    campi_db = CampusDB().select().where((CampusDB.nome == nome) & (CampusDB.inst_id == instid))

    if campi_db.exists():
        return CampusModeloPost(id=campi_db.first().id, status=False)
    id_temp = CampusDB().insert(nome=nome, inst_id=instid).execute()
    return CampusModeloPost(id=id_temp, status=True)
