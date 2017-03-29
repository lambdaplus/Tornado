# coding=utf-8
import os.path
import collections

from tornado import httpserver, web, ioloop, locale

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class Application(web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/recommended/', RecommendedHandler), ]

        settings = dict(
            templates_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules={'Book': BookModule},
            debug=True
        )
        web.Application.__init__(self, handlers, **settings)


class MainHandler(web.RequestHandler):

    def get(self):
        self.render(
            'templates/index.html',
            page_title="Lambda's Books | Home",
            header_text="Welcome to Lambda's Books!",
        )


class RecommendedHandler(web.RequestHandler):

    def get(self):
        self.render(
            'templates/recommended.html',
            page_title="Lambda's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=[
                {
                    "title": "Programming Collective Intelligence",
                    "subtitle": "Building Smart Web 2.0 Applications",
                    "img": "/static/images/lrg.jpg",
                    "author": "Toby Segaran",
                    "date_added": 1310248056,
                    "date_released": "August 2007",
                    "isbn": "978-0-596-52932-1",
                    "description": "<p>This fascinating book demonstrates how you! can build web \
                    applications to mine the enormous amount of data created by people on the Internet. \
                    With the sophisticated algorithms in this book, you can write smart \
                    programs to access interesting datasets from other web sites, collect data \
                    from users of your own applications, and analyze and understand \
                    the data once you have found it.</p>"
                },
            ]
        )


class BookModule(web.UIModule):

    def render(self, book):
        return self.render_string(
            'templates/modules/book.html',
            book=book,
        )


if __name__ == '__main__':
    options.parse_command_line()
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
