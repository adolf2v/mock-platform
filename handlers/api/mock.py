# coding:utf8

import tornado.web
from conf.redis_proxy import get_redis_client
from tornado.log import app_log
import simplejson as json
import redis

# 用来设置mock请求的配置，包括域名，接口，标识符，请求参数，响应内容
class MockHandler(tornado.web.RequestHandler):
    # 在redis中设置需要mock请求的response
    def post(self):
        # 获取设置redis中key需要参数
        # 获取域名
        host = self.get_argument("host", None)
        # 获取接口
        api = self.get_argument("api", None)
        # 获取唯一的标识符，没有也没有关系
        identifier = self.get_body_argument('id', None)
        # 获取param参数,param是一般是json串，和identer配合，获取唯一的标识符进行key的设定
        param = self.get_argument('param', None)
        # 获取设定的响应内容
        response = self.get_argument('response', None)
        # 必填的参数进行判断
        if not host or not api or not response:
            self.write(u"参数不能为空")
            return
        try:
            keyidentifier = json.loads(param).get(identifier)
            # 判断是否有标识符，并根据此进行key的组合
            if identifier and param:
                key = "%s:%s:%s" % (host, api, keyidentifier)
            else:
                key = "%s:%s" % (host, api)
            # 获取redis连接
            redis_client = get_redis_client()
            # 设置
            r = redis_client.set(key, response)
            # 判断设置是否成功
            if r:
                self.write(u"设置成功" + key)
                return
            else:
                self.write(u"设置失败，请重新设置")
                return
        except json.JSONDecodeError as e:
            app_log.error("%s", str(e))
        except redis.ConnectionError as e:
            app_log.error('%s', str(e))

# 用来处理mock的第三方请求，需要根据自己的实际情况进行改动
# 对于支付的需求，有可能需要模拟支付的回调
class Mock(tornado.web.RequestHandler):
    # 用来mock get请求，get请求过会走这里
    def get(self):
        # 用来获取请求的uri，可以用来判断请求的url
        # self.request.uri
        ohost = self.request.host
        # 此处因为有端口，所以采用了分隔符，去掉端口
        # 其实应该采用nginx的方向代理，这时候就不会带上端口，无需做下边的处理
        host = ohost.split(':')[0]
        # 获取请求的uri，不包含域名部分
        api = self.request.uri
        identifier = self.get_argument("id", None)
        param = self.get_argument('param', None)
        try:
            keyidentifier = json.loads(param).get(identifier)
            if identifier and param:
                key = "%s:%s:%s" % (host, api, keyidentifier)
            else:
                key = "%s:%s" % (host, api)
            redis_client = get_redis_client()
            r = redis_client.get(key)
            if r:
                self.write(r)
                return
            else:
                self.write("bye bye")
                return
        except json.JSONDecodeError as e:
            app_log.error("%s", str(e))
        except redis.ConnectionError as e:
            app_log.error('%s', str(e))

    # 用来mock post请求，post的请求走这里
    def post(self):
        ohost = self.request.host
        param = self.request.body_arguments
        api = self.request.uri
        # 根据action来判断
        action = self.get_body_argument('action')
        try:
            if action:
                key = "%s:%s:%s" % (ohost, api, action)
            else:
                key = "%s:%s" % (ohost, api)
            redis_client = get_redis_client()
            r = redis_client.get(key)
            self.write(r)
            return
        except json.JSONDecodeError as e:
            app_log.error("%s", str(e))
        except redis.ConnectionError as e:
            app_log.error("%s", str(e))
        except redis.RedisError as e:
            app_log.error("%s", str(e))
