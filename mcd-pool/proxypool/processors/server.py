# -*- coding: utf-8 -*-
"""
author:Lin
"""
from flask import Flask, g, request
from proxypool.storages.redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED, API_KEY, IS_DEV
import functools

#初始化flask
__all__ = ['app']

app = Flask(__name__)
if IS_DEV:
    app.debug = True


def auth_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        # conditional decorator, when setting API_KEY is set, otherwise just ignore this decorator
        if API_KEY == "":
            return func(*args, **kwargs)
        if request.headers.get('API-KEY', None) is not None:
            api_key = request.headers.get('API-KEY')
        else:
            return {"message": "请在头文件提供API KEY"}, 400
        # Check if API key is correct and valid
        if request.method == "GET" and api_key == API_KEY:
            return func(*args, **kwargs)
        else:
            return {"message": "API KEY无效"}, 403

    return decorator


def get_conn():
    """
    获取redis客户端对象
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
@auth_required
def index():
    """
    get home page, you can define your own templates
    :return:
    """
    return '<h2>Welcome to Proxy Pool System(代理池系统)</h2>'


@app.route('/random')
@auth_required
def get_proxy():
    """
    get a random proxy,显示代理以供使用
    :return: get a random proxy
    """
    conn = get_conn()
    return conn.random().string()


@app.route('/all')
@auth_required
def get_proxy_all():
    """
    get a random proxy
    映射ip
    :return: get a random proxy
    """
    conn = get_conn()
    proxies = conn.all()
    proxies_string = ''
    if proxies:
        for proxy in proxies:
            proxies_string += str(proxy) + '\n'

    return proxies_string


@app.route('/count')
@auth_required
def get_count():
    """
    代理ip的数量
    :return: count, int
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
