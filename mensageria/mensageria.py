import datetime
from typing import List

import jwt
from fastapi import APIRouter, Depends

from autenticacao.autenticacao import usuario_jwt
from config import Settings
from mensageria.mensageria_db import ConversaDb, MensagemDb, MensagemStatusDb
from mensageria.mensageria_modelos import ConversaIniciadaModelo, MensagemEnviadaModelo, ConversaModelo, MensagemModelo
from usuario.usuario_db import UsuarioDb

router = APIRouter(prefix="/mensageria",
                   tags=["Mensageria"])
settings = Settings()


@router.post('/iniciar_conversa', response_model=ConversaIniciadaModelo)
def iniciar_conversa(enc_jwt: str, receptor_id: int):
    usuario_payload = jwt.decode(enc_jwt, key=settings.jwt_secret, algorithms=["HS256"])

    autor_id = usuario_payload["id"]

    conversa = ConversaDb().select() \
        .where(ConversaDb.autor_id == autor_id & ConversaDb.receptor_id == receptor_id)
    if conversa.exists():
        return ConversaIniciadaModelo(status=False,
                                      erro='Conversa já existe')
    else:
        conversa_id = ConversaDb.insert(autor_id=autor_id,
                                        receptor_id=receptor_id).execute()

        return ConversaIniciadaModelo(status=True,
                                      conversa_id=conversa_id)


@router.post('/enviar_mensagem', response_model=MensagemEnviadaModelo)
def enviar_mensagem(conversa_id: int, conteudo: str, current_user: UsuarioDb = Depends(usuario_jwt)):
    autor_id = current_user.id.id

    conversa = ConversaDb().select().where(ConversaDb.id == conversa_id).first()
    mensagem_id = MensagemDb.insert(conteudo=conteudo,
                                    conversa_id=conversa_id,
                                    responsavel=1 if autor_id == conversa.autor_id else 2).execute()
    MensagemStatusDb.insert(mensagem_id=mensagem_id,
                            status=0,
                            aconteceu_em=datetime.datetime.now()).execute()
    print(mensagem_id)
    return MensagemEnviadaModelo(status=True,
                                 mensagem_id=mensagem_id)


@router.get('/listar_conversas', response_model=List[ConversaModelo])
def listar_conversas(current_user: UsuarioDb = Depends(usuario_jwt)):
    inicio = datetime.datetime.now()
    conversas = []
    for conversas_db in [current_user.conversas_iniciadas, current_user.conversas_convidadas]:
        for conversa_db in [*conversas_db]:
            ultima_mensagem_status = MensagemStatusDb() \
                .select() \
                .where(MensagemStatusDb.mensagem_id << conversa_db.mensagens) \
                .order_by(MensagemStatusDb.aconteceu_em.desc()) \
                .first()
            e_autor = conversa_db.autor_id.id.id == current_user.id.id

            conversa_modelo = ConversaModelo(id=conversa_db.id,
                                             autor_id=conversa_db.autor_id.id.id,
                                             autor_nome=conversa_db.autor_id.id.nome,
                                             autor_cor=conversa_db.autor_id.cor,
                                             receptor_id=conversa_db.receptor_id.id.id,
                                             receptor_nome=conversa_db.receptor_id.id.nome,
                                             receptor_cor=conversa_db.receptor_id.cor,
                                             e_autor=e_autor,
                                             ultima_mensagem_horario=ultima_mensagem_status.aconteceu_em,
                                             ultima_mensagem=ultima_mensagem_status.mensagem_id.conteudo)
            conversas.append(conversa_modelo)
    print(datetime.datetime.now() - inicio)
    return conversas


@router.get('/listar_mensagens', response_model=List[MensagemModelo])
def listar_mensagens(conversa_id: int, current_user: UsuarioDb = Depends(usuario_jwt)):
    mensagems_db = MensagemDb(
    ).select() \
        .join(MensagemStatusDb) \
        .where(MensagemDb.conversa_id == conversa_id)

    mensagems = [MensagemModelo(id=mensagem_db.id,
                                conteudo=mensagem_db.conteudo,
                                conversa_id=mensagem_db.conversa_id.id,
                                responsavel=mensagem_db.responsavel,

                                aconteceu_em=mensagem_db.status.get().aconteceu_em) for mensagem_db in mensagems_db]
    print(mensagems)
    return mensagems
