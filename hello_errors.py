# coding=utf-8
from tornado import web, httpserver, ioloop

from tornado.options import define, options

define('port', default=8000, help='run on the given port', type=int)


class IndexHandler(web.RequestHandler):

    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

    def write_error(self, status_code, **kwd):
        self.write("It's a pity! You cause a {} error!".format(status_code))


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=[(r'/', IndexHandler)], debug=True)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
