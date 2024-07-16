# -*- coding: utf-8 -*-
"""
author:Lin
读取数据库的配置
"""
import redis
import yaml
from pymysql import *


def load_config():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_redis_connection(config):

    redis_config = config.get('redis', {})


    host = redis_config.get('host', 'localhost')
    port = redis_config.get('port', 6379)

    db = redis_config.get('db', 0)

    password = redis_config.get('password', None)

    redis_client = redis.StrictRedis(host=host, port=port, db=db, password=password)
    return redis_client

def get_mysql_connection(config):

    mysql_config = config.get('mysql', {})

    host = mysql_config.get('host', 'localhost')
    port = mysql_config.get('port', 3306)

    database = mysql_config.get('database', None)

    user = mysql_config.get('user', None)
    password = mysql_config.get('password', None).encode('utf-8')

    charset = mysql_config.get('charset', None)
    
    mysql_connection = connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        charset=charset
    )
    return mysql_connection


def get_mysql_connection_init(config):
    mysql_config = config.get('mysql', {})
    host = mysql_config.get('host', 'localhost')
    port = mysql_config.get('port', 3306)
    user = mysql_config.get('user', None)
    password = mysql_config.get('password', None).encode('utf-8')
    charset = mysql_config.get('charset', None)
    mysql_connection = connect(
        host=host,
        port=port,
        user=user,
        password=password,
        charset=charset
    )
    return mysql_connection








