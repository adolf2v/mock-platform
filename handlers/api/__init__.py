#!coding:utf8
from handlers.api.indexhandler import IndexHandler
from handlers.api.mock import MockHandler
from handlers.api.mock import Mock

handlers = [(r'/', IndexHandler),
            (r'/config', MockHandler),
            (r'/.*', Mock)]
