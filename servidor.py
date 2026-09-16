import tornado.websocket

from protocolo import codificar, decodificar


class BetWebSocket(tornado.websocket.WebSocketHandler):

    clientes = set()

    def open(self):
        self.clientes.add(self)

        print("Cliente conectado")

        mensagem = codificar(
            "sistema",
            {
                "mensagem": "Novo usuário conectado."
            }
        )

        self.enviar_para_todos(mensagem)

    def on_message(self, mensagem):
        try:
            dados = decodificar(mensagem)

            if dados["tipo"] == "aposta":

                aposta = dados["dados"]

                usuario = aposta["usuario"]
                time = aposta["time"]
                valor = aposta["valor"]

                print(
                    f"{usuario} apostou R$ {valor} em {time}"
                )

                resposta = codificar(
                    "nova_aposta",
                    aposta
                )

                self.enviar_para_todos(resposta)

        except Exception as erro:
            print("Erro:", erro)

    def on_close(self):
        self.clientes.discard(self)

        print("Cliente desconectado")

    def enviar_para_todos(self, mensagem):
        for cliente in list(self.clientes):
            try:
                cliente.write_message(mensagem)
            except:
                self.clientes.discard(cliente)

    def check_origin(self, origin):
        return True