import tornado.websocket
import tornado.ioloop

from protocolo import codificar, decodificar


class BetWebSocket(tornado.websocket.WebSocketHandler):

    clientes = set()
    usuarios = {}
    apostas = []

    SALDO_INICIAL = 1000

    # Resultado aparece 40 segundos após a primeira aposta
    TEMPO_RESULTADO = 40

    # Jogos e resultados já definidos
    jogos = {

        "gremio-inter": {
            "times": [
                "Grêmio",
                "Internacional"
            ],
            "vencedor": "Internacional",
            "resultado_publicado": False,
            "timer_iniciado": False
        },

        "fla-palmeiras": {
            "times": [
                "Flamengo",
                "Palmeiras"
            ],
            "vencedor": "Palmeiras",
            "resultado_publicado": False,
            "timer_iniciado": False
        },

        "corinthians-sao-paulo": {
            "times": [
                "Corinthians",
                "São Paulo"
            ],
            "vencedor": "São Paulo",
            "resultado_publicado": False,
            "timer_iniciado": False
        }
    }


    # Executado quando um cliente conecta
    def open(self):

        self.clientes.add(self)

        self.usuario = None

        print("Novo cliente conectado")


    # Recebe as mensagens enviadas pelo JavaScript
    def on_message(self, mensagem):

        try:

            dados = decodificar(mensagem)

            tipo = dados.get("tipo")

            conteudo = dados.get(
                "dados",
                {}
            )

            if tipo == "entrar":

                self.registrar_usuario(
                    conteudo
                )

            elif tipo == "aposta":

                self.realizar_aposta(
                    conteudo
                )

        except Exception as erro:

            print("Erro:", erro)

            self.enviar_erro(
                "Não foi possível processar a mensagem."
            )


    # Registra o usuário
    def registrar_usuario(self, dados):

        nome = dados.get(
            "usuario",
            ""
        ).strip()

        if not nome:

            self.enviar_erro(
                "Informe um nome."
            )

            return

        self.usuario = nome

        # Se for um usuário novo, começa com R$ 1000
        if nome not in self.usuarios:

            self.usuarios[nome] = (
                self.SALDO_INICIAL
            )

        self.write_message(
            codificar(
                "usuario_registrado",
                {
                    "usuario": nome,
                    "saldo": self.usuarios[nome]
                }
            )
        )

        print(
            f"{nome} entrou no sistema"
        )


    # Processa uma aposta
    def realizar_aposta(self, dados):

        if self.usuario is None:

            self.enviar_erro(
                "Entre no sistema antes de apostar."
            )

            return

        jogo = dados.get("jogo")
        time = dados.get("time")
        valor = dados.get("valor")
        odd = dados.get("odd")

        # Verifica se o jogo existe
        if jogo not in self.jogos:

            self.enviar_erro(
                "Jogo inválido."
            )

            return

        # Não permite apostar depois do resultado
        if self.jogos[jogo]["resultado_publicado"]:

            self.enviar_erro(
                "Esse jogo já foi encerrado."
            )

            return

        try:

            valor = float(valor)
            odd = float(odd)

        except (TypeError, ValueError):

            self.enviar_erro(
                "Valor ou odd inválidos."
            )

            return

        # Verifica se o time pertence ao jogo
        if time not in self.jogos[jogo]["times"]:

            self.enviar_erro(
                "Time inválido."
            )

            return

        # Não permite valores negativos ou zero
        if valor <= 0:

            self.enviar_erro(
                "O valor deve ser maior que zero."
            )

            return

        saldo_atual = self.usuarios[
            self.usuario
        ]

        # Verifica o saldo
        if valor > saldo_atual:

            self.enviar_erro(
                "Saldo insuficiente."
            )

            return

        # Desconta o valor apostado
        self.usuarios[
            self.usuario
        ] -= valor

        # Registra a aposta
        aposta = {

            "usuario": self.usuario,

            "jogo": jogo,

            "time": time,

            "valor": valor,

            "odd": odd,

            "resultado": "Pendente"
        }

        self.apostas.append(
            aposta
        )

        print(
            f"{self.usuario} apostou "
            f"R$ {valor:.2f} em {time}"
        )

        # Atualiza o saldo do usuário
        self.write_message(
            codificar(
                "saldo_atualizado",
                {
                    "saldo":
                    self.usuarios[
                        self.usuario
                    ]
                }
            )
        )

        # Mostra a aposta para todos
        self.enviar_para_todos(
            codificar(
                "nova_aposta",
                aposta
            )
        )

        # Inicia o temporizador somente na primeira aposta
        if not self.jogos[jogo]["timer_iniciado"]:

            self.jogos[jogo][
                "timer_iniciado"
            ] = True

            print(
                f"Resultado de {jogo} "
                f"será divulgado em "
                f"{self.TEMPO_RESULTADO} segundos."
            )

            tornado.ioloop.IOLoop.current().call_later(

                self.TEMPO_RESULTADO,

                self.publicar_resultado,

                jogo
            )


    # Publica o resultado depois dos 40 segundos
    def publicar_resultado(self, jogo):

        dados_jogo = self.jogos[jogo]

        if dados_jogo["resultado_publicado"]:

            return

        vencedor = dados_jogo[
            "vencedor"
        ]

        dados_jogo[
            "resultado_publicado"
        ] = True

        print(
            f"Resultado de {jogo}: "
            f"{vencedor} venceu!"
        )

        # Verifica todas as apostas daquele jogo
        for aposta in self.apostas:

            if aposta["jogo"] != jogo:

                continue

            # Aposta vencedora
            if aposta["time"] == vencedor:

                premio = (
                    aposta["valor"]
                    *
                    aposta["odd"]
                )

                self.usuarios[
                    aposta["usuario"]
                ] += premio

                aposta[
                    "resultado"
                ] = "Ganhou"

                print(
                    f"{aposta['usuario']} ganhou "
                    f"R$ {premio:.2f}"
                )

            # Aposta perdedora
            else:

                aposta[
                    "resultado"
                ] = "Perdeu"

                print(
                    f"{aposta['usuario']} perdeu a aposta"
                )

        # Envia o resultado para todos os clientes
        self.enviar_para_todos(
            codificar(
                "resultado_jogo",
                {
                    "jogo": jogo,
                    "vencedor": vencedor
                }
            )
        )

        # Atualiza os saldos depois do resultado
        self.atualizar_saldos()


    # Envia o saldo atualizado para cada usuário
    def atualizar_saldos(self):

        for cliente in list(
            self.clientes
        ):

            if (
                cliente.usuario
                in self.usuarios
            ):

                cliente.write_message(
                    codificar(
                        "saldo_atualizado",
                        {
                            "saldo":
                            self.usuarios[
                                cliente.usuario
                            ]
                        }
                    )
                )


    # Envia mensagem de erro
    def enviar_erro(self, mensagem):

        self.write_message(
            codificar(
                "erro",
                {
                    "mensagem": mensagem
                }
            )
        )


    # Envia uma mensagem para todos os clientes conectados
    def enviar_para_todos(
        self,
        mensagem
    ):

        for cliente in list(
            self.clientes
        ):

            try:

                cliente.write_message(
                    mensagem
                )

            except Exception:

                self.clientes.discard(
                    cliente
                )


    # Executado quando o cliente desconecta
    def on_close(self):

        self.clientes.discard(
            self
        )

        if self.usuario:

            print(
                f"{self.usuario} desconectou"
            )

        else:

            print(
                "Cliente desconectado"
            )


    def check_origin(
        self,
        origin
    ):

        return True