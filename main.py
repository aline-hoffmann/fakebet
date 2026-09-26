import os

import tornado.ioloop
import tornado.web

from servidor import BetWebSocket


BASE_DIR = os.path.dirname(__file__)

# Handler responsável por carregar a página inicial
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("static/index.html")

# Cria e configura a aplicação Tornado
def criar_aplicacao():

    return tornado.web.Application([
        # Rota principal da aplicação
        (r"/", MainHandler),

        # Rota utilizada para estabelecer a conexão WebSocket
        (r"/websocket", BetWebSocket),
        # Permite o acesso aos arquivos estáticos da aplicação
        (
            r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {
                "path": os.path.join(BASE_DIR, "static")
            }
        )
    ])

# Executa o servidor quando este arquivo é iniciado diretamente
if __name__ == "__main__":

    app = criar_aplicacao()

    app.listen(8888)

    print("================================")
    print("        FAKEBET INICIADA")
    print("================================")
    print("Acesse: http://localhost:8888")

    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":

    app = criar_aplicacao()

    app.listen(8888)

    print("FakeBet rodando!")
    print("Acesse: http://localhost:8888")

    # Mantém o servidor executando e aguardando conexões e eventos
    tornado.ioloop.IOLoop.current().start()
