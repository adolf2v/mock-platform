# mock-platform
## mock平台

用来mock第三方请求，用redis来存储

启动```python server.py```

访问127.0.0.1:9528（可以在nginx配置域名：mock.himi.com）,可以配置mock接口的信息

在nginx配置第三方域名，反向代理到自己启动的tronado实例上