# coding=utf-8\
import os.path

from tornado import web, httpserver, ioloop

from tornado.options import define, options
define('port', default=8000, help='run on the given port', type=int)


class Application(web.Application):

    def __init__(self):
        handlers = [
            (r'/', WelcomeHandler),
            (r'/login', LoginHandler),
            (r'/logout', LogoutHandler)]

        settings = {
            'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
            'cookie_secret': 'f0008374-f3ec-455d-a57e-73e49a82e106',
            'xrsf_cookies': True,
            'login_url': "/login",
            'debug': True}
        web.Application.__init__(self, handlers, **settings)


class BaseHandler(web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie('username')


class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie('username', self.get_argument('username'))
        self.redirect('/')


class WelcomeHandler(BaseHandler):

    @web.authenticated
    def get(self):
        self.render('index.html', user=self.current_user)


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie('username')
        self.redirect('/')


if __name__ == '__main__':
    options.parse_command_line()
    http_server = httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
