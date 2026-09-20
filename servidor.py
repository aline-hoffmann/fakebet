import tornado.websocket

from protocolo import codificar, decodificar


class BetWebSocket(tornado.websocket.WebSocketHandler):

    clientes = set()
    usuarios = {}
    apostas = []

    SALDO_INICIAL = 1000

    def open(self):
        self.clientes.add(self)
        self.usuario = None

        print("Novo cliente conectado")

    def on_message(self, mensagem):
        try:
            dados = decodificar(mensagem)

            tipo = dados.get("tipo")
            conteudo = dados.get("dados", {})

            if tipo == "entrar":
                self.registrar_usuario(conteudo)

            elif tipo == "aposta":
                self.realizar_aposta(conteudo)

        except Exception as erro:
            print("Erro:", erro)

            self.write_message(
                codificar(
                    "erro",
                    {
                        "mensagem": "Não foi possível processar a mensagem."
                    }
                )
            )

    def registrar_usuario(self, dados):
        nome = dados.get("usuario", "").strip()

        if not nome:
            self.write_message(
                codificar(
                    "erro",
                    {
                        "mensagem": "Informe um nome."
                    }
                )
            )
            return

        self.usuario = nome

        if nome not in self.usuarios:
            self.usuarios[nome] = self.SALDO_INICIAL

        self.write_message(
            codificar(
                "usuario_registrado",
                {
                    "usuario": nome,
                    "saldo": self.usuarios[nome]
                }
            )
        )

        print(f"{nome} entrou no sistema")

    def realizar_aposta(self, dados):
        if self.usuario is None:
            self.write_message(
                codificar(
                    "erro",
                    {
                        "mensagem": "Entre no sistema antes de apostar."
                    }
                )
            )
            return

        time = dados.get("time")
        valor = dados.get("valor")
        odd = dados.get("odd")

        try:
            valor = float(valor)
            odd = float(odd)
        except (TypeError, ValueError):
            self.enviar_erro("Valor ou odd inválidos.")
            return

        if not time:
            self.enviar_erro("Escolha um time.")
            return

        if valor <= 0:
            self.enviar_erro("O valor da aposta deve ser maior que zero.")
            return

        saldo_atual = self.usuarios[self.usuario]

        if valor > saldo_atual:
            self.enviar_erro("Saldo insuficiente.")
            return

        self.usuarios[self.usuario] -= valor

        aposta = {
            "usuario": self.usuario,
            "time": time,
            "valor": valor,
            "odd": odd
        }

        self.apostas.append(aposta)

        print(
            f"{self.usuario} apostou "
            f"R$ {valor:.2f} em {time}"
        )

        self.write_message(
            codificar(
                "saldo_atualizado",
                {
                    "saldo": self.usuarios[self.usuario]
                }
            )
        )

        mensagem = codificar(
            "nova_aposta",
            aposta
        )

        self.enviar_para_todos(mensagem)

    def enviar_erro(self, mensagem):
        self.write_message(
            codificar(
                "erro",
                {
                    "mensagem": mensagem
                }
            )
        )

    def enviar_para_todos(self, mensagem):
        clientes_desconectados = []

        for cliente in self.clientes:
            try:
                cliente.write_message(mensagem)
            except Exception:
                clientes_desconectados.append(cliente)

        for cliente in clientes_desconectados:
            self.clientes.discard(cliente)

    def on_close(self):
        self.clientes.discard(self)

        if self.usuario:
            print(f"{self.usuario} desconectou")
        else:
            print("Cliente desconectado")

    def check_origin(self, origin):
        return True