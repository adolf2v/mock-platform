#!coding:utf8
from handlers.api.indexhandler import IndexHandler
from handlers.api.mock import MockHandler
from handlers.api.mock import Mock
# "/.*"是用来接收第三方mock请求的，然后再进行处理
handlers = [(r'/', IndexHandler),
            (r'/config', MockHandler),
            (r'/.*', Mock)]
