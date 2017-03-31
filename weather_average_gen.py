# coding=utf-8
import datetime
import time
import json
import urllib


from tornado import web, httpserver, ioloop, httpclient, gen

from tornado.options import options, define
define('port', default=8000, help='run on the given port', type=int)


key = 'ce784abd0df64e7696cec61ccea854d3'
url = 'https://free-api.heweather.com/v5/forecast?'


class IndexHandler(web.RequestHandler):

    @gen.coroutine
    def get(self):
        query = self.get_argument('city')
        client = httpclient.AsyncHTTPClient()
        response = yield client.fetch(url + urllib.parse.urlencode({'city': query, 'key': key}))
        body = json.loads(response.body)
        three_weather = body['HeWeather5'][0]['daily_forecast']
        three_tmp = [w['tmp'] for w in three_weather]
        max_tmp = sum(int(t['max']) for t in tmp) / 3
        min_tmp = sum(int(t['min']) for t in tmp) / 3
        avage_tmp = sum([max_tmp, min_tmp]) / 2
        self.write('''
            <div style='text-align: center'>
                <div style='font-size: 72px'>{}</div>
                <div style='font-size: 72px'>Max: {:.2f} ℃</div>
                <div style='font-size: 72px'>Min: {:.2f} ℃</div>
                <div style='font-size: 144px'>Avg: {:.2f} ℃</div>
                <div style='font-size: 24px'>The Temperature</div>
            </div>'''.format(self.get_argument('city'), max_tmp, min_tmp, avage_tmp))
        self.finish()


if __name__ == '__main__':
    options.parse_command_line()
    app = web.Application(handlers=[(r'/', IndexHandler)], debug=True)
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        exit()
