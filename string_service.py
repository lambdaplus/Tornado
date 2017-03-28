# coding=utf-8
import textwrap

from tornado import httpserver, ioloop, web

from tornado.options import define, options

define('port', default=8000, help='run on the given port', type=int)


class ReverseHandler(web.RequestHandler):

    def get(self, input):
        self.write(input[::-1])


class WrapperHandler(web.RequestHandler):

    def post(self):
        text = self.get_argument('text')
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(
        handlers=[
            (r'/reverse/(\w+)', ReverseHandler),
            (r'/wrap', WrapperHandler),
        ], debug=True)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
