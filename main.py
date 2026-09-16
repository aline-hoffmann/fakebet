import os
import tornado.ioloop
import tornado.web

from servidor import BetWebSocket


BASE_DIR = os.path.dirname(__file__)


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("static/index.html")


def criar_aplicacao():

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", BetWebSocket),
        (
            r"/static/(.*)",
            tornado.web.StaticFileHandler,
            {
                "path": os.path.join(BASE_DIR, "static")
            }
        )
    ])


if __name__ == "__main__":

    app = criar_aplicacao()

    app.listen(8888)

    print("FakeBet rodando!")
    print("Acesse: http://localhost:8888")

    tornado.ioloop.IOLoop.current().start()