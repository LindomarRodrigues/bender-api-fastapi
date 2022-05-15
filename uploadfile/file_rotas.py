import shutil
from typing import Optional, List
from config import Settings
from fastapi import APIRouter, Depends, Body, File, UploadFile

from uploadfile.file_db import File
from uploadfile.file_modelos import FileModelo

router = APIRouter(prefix="/files",
                   tags=["Files"])
settings = Settings()

@router.post('/files', response_model=FileModelo)
def files(payload: dict = Body(...)):
    id_temp = File().insert(arquivo=payload['arquivo']).execute()
    return FileModelo(arquivo=payload['arquivo'], id=id_temp)

@router.post('/uploadfile')
def create_upload_file(arquivo: UploadFile):
    with open(f'{arquivo.filename}', 'wb') as buffer:
        shutil.copyfileobj(arquivo.file, buffer)
    return {"arquivo": arquivo.filename}
    
@router.get('/file', response_model=FileModelo)
def files(arquivo_id: int):
    arquivo = File().select().where(File.id==arquivo_id).first()


    return FileModelo(arquivo=arquivo.arquivo, id=arquivo.id)


@router.get('/files', response_model=List[FileModelo])
def files():
    arquivos = File().select()

    arquivos_modelos = []
    for arquivo in arquivos:
        arquivos_modelos.append(FileModelo(arquivo=arquivo.arquivo, id=arquivo.id))
    return arquivos_modelos