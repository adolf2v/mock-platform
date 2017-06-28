#!coding:utf8

import tornado.web

# 跳转到config.html的页面
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('config.html')
