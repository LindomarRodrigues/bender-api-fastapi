import email
import imp
from os import stat
from typing import List
from config import Settings
from fastapi import APIRouter, Body

from lattesDocente.lattesDocente_db import lattesDocenteDB
from lattesDocente.lattesDocente_modelos import LattesGetDocenteModelo
from lattesDocente.lattesDocente_modelos import LattesPostDocenteModelo

router = APIRouter(prefix="/lattesDocente",
                   tags=["Lattes dos Docentes"])
settings = Settings()

@router.get('/lattesDocente', response_model=List[LattesGetDocenteModelo])
def latte():
    lattes = lattesDocenteDB().select()
    lattes_modelo = []
    for contato in lattes:
        lattes_modelo.append(LattesGetDocenteModelo(id= lattes.id, nome= lattes.nome, lattes= lattes.lattes))
    return lattes_modelo

@router.post('/lattesDocente', response_model=LattesPostDocenteModelo)
def latte(response: dict = Body(...)):
    lattes_db = lattesDocenteDB().select().where((lattesDocenteDB.nome == response['nome'])&(lattesDocenteDB.lattes == response['lattes']))

    if lattes_db.exists():
        return LattesPostDocenteModelo(id = lattes_db.first().id, status = False)
    id_temp = lattesDocenteDB().insert(nome = response['nome'], lattes = response['lattes']).execute()
    return LattesPostDocenteModelo(id = id_temp, status= True)
