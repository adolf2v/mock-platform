#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis

from tornado.options import options

__all__ = ['init_redis_client', 'get_redis_client']
_redis_client = None


def init_redis_client(host, port, force=False):
    global _redis_client
    if force or not _redis_client:
        _redis_client = redis.Redis(host=host, port=port)

        return _redis_client
    return _redis_client


def get_redis_client():
    global _redis_client
    if not _redis_client:
        init_redis_client(options.redis_host, options.redis_port)
    return _redis_client
