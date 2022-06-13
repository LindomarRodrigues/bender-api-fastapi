from typing import List
from config import Settings
from fastapi import APIRouter, Body

from regimentoAcademico.regimento_db import RegimentoDB 
from regimentoAcademico.regimento_modelos import RegimentoModeloPost
from regimentoAcademico.regimento_modelos import RegimentoModeloGet

router = APIRouter(prefix="/regimento",   
                   tags=["regimento"]) 
settings = Settings()

@router.post('/regimento', response_model=RegimentoModeloPost)
def regimentos(payload: dict = Body(...)):
    print(payload)
    regimento_db = RegimentoDB().select().where((RegimentoDB.periodo == payload['periodo'])&(RegimentoDB.horario == payload['disciplina'])&(RegimentoDB.disciplina == payload['horario']))
    if regimento_db.exists():
        return RegimentoModeloPost(id = regimento_db.first().id, status=False)
    id_temp = RegimentoDB().insert(periodo = payload['periodo'], disciplina=payload['disciplina'], horario = payload['horario']).execute()
    return RegimentoModeloPost(id = id_temp, status=True)

@router.get('/listar_regimento', response_model=List[RegimentoModeloGet])
def regimentos():
    regs_academico = RegimentoDB().select()
    regimento_modelo = []
    for reg in regs_academico:
        regimento_modelo.append(RegimentoModeloGet(id = reg.id, periodo = reg.periodo, disciplina= reg.disciplina, horario= reg.horario))
    return regimento_modelo