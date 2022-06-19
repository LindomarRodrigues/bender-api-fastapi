from typing import Optional
import os
from fastapi import APIRouter, Depends, File

from autenticacao.autenticacao import usuario_jwt
from config import Settings
from starlette.responses import FileResponse
from starlette.background import BackgroundTasks
from informacoes_curso.informacoes_curso_db import InformacoesCursoDB
from informacoes_curso.informacoes_curso_modelos import InformacoesCursoPost

from usuario.usuario_db import UsuarioDb, TipoUsuarioDB
router = APIRouter(prefix="/informacoes_curso",
                   tags=["Informações do curso"])
settings = Settings()


@router.post('/calendario_academico', response_model=InformacoesCursoPost)
async def predict(pdf: bytes = File (...), current_user: UsuarioDb = Depends(usuario_jwt)):
    nome = "calendario"
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return InformacoesCursoPost(status= False, error="Usuario não autenticado")
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == nome))
    if not query.exists():
        result = InformacoesCursoDB().insert(pdf_name = nome, pdf = pdf).execute()
        return InformacoesCursoPost(status= True, id = result)
    else:
        result = InformacoesCursoDB().update(pdf_name = nome, pdf = pdf).where(InformacoesCursoDB.pdf_name == nome).execute()
        return InformacoesCursoPost(status= True, id = result)

@router.get('/calendario_academico')
async def get_pdf(bg_tasks: BackgroundTasks):
    name = "calendario"
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == name))
    result= query.first()
    path = result.pdf_name + ".pdf"
    text_file = open(path, "wb")
    text_file.write(result.pdf)
    text_file.close()
    bg_tasks.add_task(os.remove, path)
    return FileResponse(path, media_type='application/pdf',filename=path, background=bg_tasks)