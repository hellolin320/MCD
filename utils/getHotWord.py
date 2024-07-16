# -*- coding: utf-8 -*-
"""
author:Lin
获取热词的相关信息
"""
import pickle
import re
import pandas as pd
import redis

from utils.myquery import myquery

def getAllHotWord():

    # 创建一个空列表
    data = []

    # 读取csv
    df=pd.read_csv('wordcount/wordTotal.csv')
    for i in df.values:
        data.append([
                # 匹配中文，匹配次数
                re.search('[\u4e00-\u9fa5]+',str(i)).group(),
                re.search('\d+',str(i)).group()
            ])
    return data

def getHotWordLen_de(hotWord):
    sql="""
        select userComment from all_reviews
    """
    commentsList=myquery(sql,[],"select")

    hotWordLen=0
    for i in commentsList:
        if i[0].find(hotWord) !=-1:
            hotWordLen+=1
    return hotWordLen

def getHotWordLen(hotWord):
    sql = """
        SELECT COUNT(*) FROM all_reviews WHERE userComment LIKE %s
    """
    hotWordWithWildcards = '%' + hotWord + '%'  # 添加通配符以进行模糊匹配

    result = myquery(sql, [hotWordWithWildcards], "select")

    hotWordLen = result[0][0] if result else 0
    return hotWordLen

def getHotWordChartData(hotWord):
    sql = """
        select userCommentTime,userComment from all_reviews
    """
    results = myquery(sql, [], "select")

    # 创建空字典存储每个年-月组合下的评论数量
    createdAt = {}
    for i in results:
        if i[1].find(hotWord) != -1:
            date_time = i[0].split()[0]  # 将日期时间字符串按空格分割并取第一部分（日期）
            year_month = date_time[:7]  # 只保留年-月部分
            if year_month not in createdAt:
                createdAt[year_month] = 1
            else:
                createdAt[year_month] += 1

    # 将日期排序
    sorted_dates = sorted(createdAt.keys())
    sorted_counts = [createdAt[date] for date in sorted_dates]

    return sorted_dates, sorted_counts


def getHotWordCommentData(hotWord):
    # 初始化Redis连接
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    cached_data = redis_client.get('hotWordCommentList')
    if cached_data:
        commentList=pickle.loads(cached_data)
        print('使用redis hWCL缓存数据')
    else:
        sql = """
            select userName,userScore,userComment,userCommentTime from all_reviews
        """
        commentList = myquery(sql, [], "select")
        

        redis_client.set('hotWordCommentList',pickle.dumps(commentList))
        redis_client.persist('hotWordCommentList')
        print('没有缓存Comment数据，载入redis')
        
    hotWordComment=[]
    for comment in commentList:
        if hotWord in comment[2]:
            hotWordComment.append(comment)
    return hotWordComment








