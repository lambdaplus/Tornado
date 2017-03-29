# coding=utf-8
import os.path

from tornado import web, httpserver, ioloop

from tornado.options import define, options

define('port', default=8000, help='run on the given port', type=int)


class IndexHandler(web.RequestHandler):

    def get(self):
        self.render('index.html')


class PoemHandler(web.RequestHandler):

    def post(self):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render('poem.html', roads=noun1, wood=noun2,
                    made=verb, difference=noun3)


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', PoemHandler)],
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    )
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
