import hashlib
import re


def verificar_email(email):
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(regex, email):
        return True
    else:
        return False


def gerar_hash_sha256(valor):
    valor_encoded = valor.encode()
    hash_encoded = hashlib.sha256(valor_encoded)
    hash_decoded = hash_encoded.hexdigest()

    return hash_decoded
