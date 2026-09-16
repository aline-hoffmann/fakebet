import json


def codificar(tipo, dados):
    mensagem = {
        "tipo": tipo,
        "dados": dados
    }

    return json.dumps(mensagem)


def decodificar(mensagem):
    return json.loads(mensagem)