import os

from fastapi import APIRouter, Depends, File
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse

from autenticacao.autenticacao import usuario_jwt
from config import Settings
from informacoes_curso.informacoes_curso_db import InformacoesCursoDB
from informacoes_curso.informacoes_curso_modelos import InformacoesCursoPost
from usuario.usuario_db import UsuarioDb, TipoUsuarioDB

router = APIRouter(prefix="/informacoes_curso",
                   tags=["Informações do curso"])
settings = Settings()

@router.get('/calendario_academico')
async def get_pdf(bg_tasks: BackgroundTasks):
    name = "calendario"
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == name))
    result = query.first()
    path = result.pdf_name + ".pdf"
    text_file = open(path, "wb")
    text_file.write(result.pdf)
    text_file.close()
    bg_tasks.add_task(os.remove, path)
    return FileResponse(path, media_type='application/pdf', filename=path, background=bg_tasks)

@router.post('/calendario_academico', response_model=InformacoesCursoPost)
async def predict(pdf: bytes = File(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    nome = "calendario"
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return InformacoesCursoPost(status=False, error="Usuario não autenticado")
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == nome))
    if not query.exists():
        result = InformacoesCursoDB().insert(pdf_name=nome, pdf=pdf).execute()
        return InformacoesCursoPost(status=True, id=result)
    else:
        result = InformacoesCursoDB().update(pdf_name=nome, pdf=pdf).where(
            InformacoesCursoDB.pdf_name == nome).execute()
        return InformacoesCursoPost(status=True, id=result)

@router.get('/auxilio_uft')
async def get_pdf(bg_tasks: BackgroundTasks):
    name = "auxilio"
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == name))
    result = query.first()
    path = result.pdf_name + ".pdf"
    text_file = open(path, "wb")
    text_file.write(result.pdf)
    text_file.close()
    bg_tasks.add_task(os.remove, path)
    return FileResponse(path, media_type='application/pdf', filename=path, background=bg_tasks)

@router.post('/auxilio_uft', response_model=InformacoesCursoPost)
async def predict(pdf: bytes = File(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    nome = "auxilio"
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return InformacoesCursoPost(status=False, error="Usuario não autenticado")
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == nome))
    if not query.exists():
        result = InformacoesCursoDB().insert(pdf_name=nome, pdf=pdf).execute()
        return InformacoesCursoPost(status=True, id=result)
    else:
        result = InformacoesCursoDB().update(pdf_name=nome, pdf=pdf).where(
            InformacoesCursoDB.pdf_name == nome).execute()
        return InformacoesCursoPost(status=True, id=result)


@router.get('/biblioteca_uft')
async def get_pdf(bg_tasks: BackgroundTasks):
    name = "biblioteca"
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == name))
    result = query.first()
    path = result.pdf_name + ".pdf"
    text_file = open(path, "wb")
    text_file.write(result.pdf)
    text_file.close()
    bg_tasks.add_task(os.remove, path)
    return FileResponse(path, media_type='application/pdf', filename=path, background=bg_tasks)

@router.post('/biblioteca_uft', response_model=InformacoesCursoPost)
async def predict(pdf: bytes = File(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    nome = "biblioteca"
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return InformacoesCursoPost(status=False, error="Usuario não autenticado")
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == nome))
    if not query.exists():
        result = InformacoesCursoDB().insert(pdf_name=nome, pdf=pdf).execute()
        return InformacoesCursoPost(status=True, id=result)
    else:
        result = InformacoesCursoDB().update(pdf_name=nome, pdf=pdf).where(
            InformacoesCursoDB.pdf_name == nome).execute()
        return InformacoesCursoPost(status=True, id=result)


@router.get('/matriz_curricular')
async def get_pdf(bg_tasks: BackgroundTasks):
    name = "matriz"
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == name))
    result = query.first()
    path = result.pdf_name + ".pdf"
    text_file = open(path, "wb")
    text_file.write(result.pdf)
    text_file.close()
    bg_tasks.add_task(os.remove, path)
    return FileResponse(path, media_type='application/pdf', filename=path, background=bg_tasks)

@router.post('/matriz_curricular', response_model=InformacoesCursoPost)
async def predict(pdf: bytes = File(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    nome = "matriz"
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return InformacoesCursoPost(status=False, error="Usuario não autenticado")
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == nome))
    if not query.exists():
        result = InformacoesCursoDB().insert(pdf_name=nome, pdf=pdf).execute()
        return InformacoesCursoPost(status=True, id=result)
    else:
        result = InformacoesCursoDB().update(pdf_name=nome, pdf=pdf).where(
            InformacoesCursoDB.pdf_name == nome).execute()
        return InformacoesCursoPost(status=True, id=result)


@router.get('/regimento_academico')
async def get_pdf(bg_tasks: BackgroundTasks):
    name = "regimento"
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == name))
    result = query.first()
    path = result.pdf_name + ".pdf"
    text_file = open(path, "wb")
    text_file.write(result.pdf)
    text_file.close()
    bg_tasks.add_task(os.remove, path)
    return FileResponse(path, media_type='application/pdf', filename=path, background=bg_tasks)

@router.post('/regimento_academico', response_model=InformacoesCursoPost)
async def predict(pdf: bytes = File(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    nome = "regimento"
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return InformacoesCursoPost(status=False, error="Usuario não autenticado")
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == nome))
    if not query.exists():
        result = InformacoesCursoDB().insert(pdf_name=nome, pdf=pdf).execute()
        return InformacoesCursoPost(status=True, id=result)
    else:
        result = InformacoesCursoDB().update(pdf_name=nome, pdf=pdf).where(
            InformacoesCursoDB.pdf_name == nome).execute()
        return InformacoesCursoPost(status=True, id=result)


@router.get('/restaurante_universitario')
async def get_pdf(bg_tasks: BackgroundTasks):
    name = "restaurante"
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == name))
    result = query.first()
    path = result.pdf_name + ".pdf"
    text_file = open(path, "wb")
    text_file.write(result.pdf)
    text_file.close()
    bg_tasks.add_task(os.remove, path)
    return FileResponse(path, media_type='application/pdf', filename=path, background=bg_tasks)
    
@router.post('/restaurante_universitario', response_model=InformacoesCursoPost)
async def predict(pdf: bytes = File(...), current_user: UsuarioDb = Depends(usuario_jwt)):
    nome = "restaurante"
    tipo_usuario_db = TipoUsuarioDB().select().where(TipoUsuarioDB.usuario_id == current_user.id).first()
    if tipo_usuario_db.tipo != 2:
        return InformacoesCursoPost(status=False, error="Usuario não autenticado")
    query = InformacoesCursoDB().select().where((InformacoesCursoDB.pdf_name == nome))
    if not query.exists():
        result = InformacoesCursoDB().insert(pdf_name=nome, pdf=pdf).execute()
        return InformacoesCursoPost(status=True, id=result)
    else:
        result = InformacoesCursoDB().update(pdf_name=nome, pdf=pdf).where(
            InformacoesCursoDB.pdf_name == nome).execute()
        return InformacoesCursoPost(status=True, id=result)


