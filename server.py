#!coding:utf8

import tornado.httpserver
import tornado.options
import tornado.ioloop
import os
from conf.redis_proxy import init_redis_client
import tornado.web
from settings import init_app_settings
from tornado.options import define, options
from handlers.api import handlers as api_handlers

define("port", default=9528, help="run on the  given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, **settings):
        self.external_ = {}
        self.external_['redis_client'] = init_redis_client(settings['redis_host'], settings['redis_port'])
        settings['template_path'] = os.path.join(os.path.dirname(__file__), 'html')
        settings['debug'] = True
        tornado.web.Application.__init__(self, handlers=api_handlers, **settings)


def main():
    tornado.options.options.logging = "debug"
    settings = init_app_settings()
    application = Application(**settings)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    instance.start()


if __name__ == '__main__':
    main()
