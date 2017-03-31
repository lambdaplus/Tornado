# coding=utf-8
import datetime
import time
import json
import urllib


from tornado import web, httpserver, ioloop, httpclient

from tornado.options import options, define
define('port', default=8000, help='run on the given port', type=int)


key = 'ce784abd0df64e7696cec61ccea854d3'
url = 'https://free-api.heweather.com/v5/forecast?'


class IndexHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        query = self.get_argument('city')
        client = httpclient.AsyncHTTPClient()
        client.fetch(url + urllib.parse.urlencode({'city': query, 'key': key}),
                                                  callback=self.on_response)

    def on_response(self, response):
        body = json.loads(response.body)
        three_weather = body['HeWeather5'][0]['daily_forecast']
        tmp = [w['tmp'] for w in three_weather]
        max_tmp = sum(int(t['max']) for t in tmp) / 3
        min_tmp = sum(int(t['min']) for t in tmp) / 3
        avage_tmp = sum([max_tmp, min_tmp]) / 2
        self.write('''
            <div style='text-align: center'>
                <div style='font-size: 72px'>{}</div>
                <div style='font-size: 72px'>{:.2f}</div>
                <div style='font-size: 72px'>{:.2f}</div>
                <div style='font-size: 144px'>{:.2f}</div>
                <div style='font-size: 24px'>tweets per second</div>
            </div>'''.format(self.get_argument('city'), max_tmp, min_tmp, avage_tmp))
        self.finish()


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=[(r'/', IndexHandler)], debug=True)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop.IOLoop.instance().start()
