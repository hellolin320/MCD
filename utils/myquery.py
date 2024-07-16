# -*- coding: utf-8 -*-
"""
author:Lin
封装SQL
"""
from pymysql import *
from utils.load_config import load_config,get_mysql_connection
conn=get_mysql_connection(load_config())
cursor=conn.cursor()

# 通用SQL
def myquery(sql,params,type="select"):

    # 转换为元组类型
    params=tuple(params)
    cursor.execute(sql,params)
    conn.ping(reconnect=True)

    #如果是查询，执行查询操作，提交事务。否则提交事务
    if type=='select':
        data_list=cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()

# 地图SQL使用
def mapquery(sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# 简单查询
def myselect(sql):
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0] if result else None
    conn.commit()
