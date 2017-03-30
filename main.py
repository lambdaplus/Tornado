# coding=utf-8
import os.path
import time
import pymongo

from tornado import httpserver, web, ioloop, locale

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class Application(web.Application):

    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/recommended/', RecommendedHandler),
            (r'/edit/([0-9Xx\-]+)', BookEditHandler),
            (r'/add', BookEditHandler),
            ]

        settings = dict(
            templates_path=os.path.join(
                os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules={'Book': BookModule},
            debug=True
        )
        conn = pymongo.MongoClient('localhost', 27017)
        self.db = conn.bookstore
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
        coll = self.application.db.books
        books = coll.find()
        self.render(
            'templates/recommended.html',
            page_title="Lambda's Books | Recommended Reading",
            header_text="Recommended Reading",
            books=books
        )

class BookEditHandler(web.RequestHandler):

    def get(self, isbn=None):
        book = dict()
        if isbn:
            coll = self.application.db.books
            book = coll.find_one({'isbn': isbn})
        self.render(
            'templates/book_edit.html',
            page_title="Lambda's Books",
            header_text="Edit book",
            book=book
        )

    def post(self, isbn=None):
        book_fields = ['isbn', 'title', 'subtitle', 'img', 'author',
        'date_released', 'description']
        coll = self.application.db.books
        book = dict()

        if isbn:
            book = coll.find_one({'isbn': isbn})
        for key in book_fields:
            book[key] = self.get_argument(key, None)

        if isbn:
            coll.save(book)
        else:
            book['date_added'] = int(time.time())
            coll.insert_one(book)
        self.redirect('/recommended/')


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
