# -*- coding: utf-8 -*-
"""
author:Lin
可视化系统
"""
import csv
import json
import pickle
import re
import logging
import redis
import pandas as pd

from snownlp import SnowNLP
from utils.getHotWord import getAllHotWord, getHotWordChartData, getHotWordLen, getHotWordCommentData
from flask import Flask, jsonify,session,render_template,redirect,Blueprint,request
from sqlalchemy import create_engine

from utils.myquery import mapquery, myquery, myselect
from utils.load_config import load_config,get_redis_connection

# 初始化Redis连接
redis_client = get_redis_connection(load_config())

pb=Blueprint('page',__name__,url_prefix='/page',template_folder='templates')

@pb.route('/home')
def home():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

    # 评论数最多的店名
    sql="""
        SELECT shopName FROM all_reviews 
        GROUP BY shopName 
        ORDER BY COUNT(userComment) DESC 
        LIMIT 1;
    """
    shopname_maxcomment = myselect(sql)

    # 总评论数
    sql="""
        select count(userComment) from all_reviews
    """
    allcomment_count = myselect(sql)

    # 最活跃区域
    sql="""
        SELECT l.shopRegion
        FROM location l
        INNER JOIN all_reviews r ON l.shopName = r.shopName
        GROUP BY l.shopRegion
        ORDER BY COUNT(r.userComment) DESC
        LIMIT 1;
    """
    active_region = myselect(sql)

    # 好评、中评、差评数量
    goodCommentSQL="""
        select count(userComment) from all_reviews where sentiment=0
    """
    middleCommentSQL = """
        select count(userComment) from all_reviews where sentiment=1
    """
    badCommentSQL = """
        select count(userComment) from all_reviews where sentiment=2
    """
    goodCommentCount=myselect(goodCommentSQL)
    middleCommentCount=myselect(middleCommentSQL)
    badCommentCount=myselect(badCommentSQL)


    # 评论时间分布
    # 连接到MySQL数据库
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/jupiter_mcd')
    # 从MySQL读取数据到DataFrame
    all_reviews_df = pd.read_sql_table('all_reviews', engine)
    # 使用正则表达式提取时间信息
    all_reviews_df['userCommentTime'] = all_reviews_df['userCommentTime'].apply(
        lambda x: re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', x)[0])
    # 转换为日期时间格式
    all_reviews_df['userCommentTime'] = pd.to_datetime(all_reviews_df['userCommentTime'],
                                                       format='%Y-%m-%d %H:%M')  # 提取评论年份
    all_reviews_df['year'] = all_reviews_df['userCommentTime'].dt.year
    # 根据年份和情感对评论进行分组和计数
    sentiment_counts = all_reviews_df.groupby(['year', 'sentiment']).size().unstack(fill_value=0)


    # 情感环形图 sh
    shsql="SELECT sentiment, COUNT(*) as count FROM all_reviews GROUP BY sentiment"
    sh = pd.read_sql_query(shsql, engine)
    # 将DataFrame中的数据转换为字典
    sh_dict = sh.set_index('sentiment')['count'].to_dict()
    sh_json = json.dumps(sh_dict)

    # 各区域店铺数量
    srsql="select count(DISTINCT a.shopName) as shopNameCount,b.shopRegion from all_reviews a join location b on a.shopName=b.shopName GROUP BY shopRegion"
    sr=pd.read_sql_query(srsql,engine)
    sr_sorted = sr.sort_values(by='shopNameCount', ascending=True) #排序
    sr_dict=sr_sorted.set_index('shopRegion')['shopNameCount'].to_dict()
    sr_json=json.dumps(sr_dict,ensure_ascii=False)

    # 食物词云
    foodData = redis_client.get('foodData')
    if foodData:
        foodData = pickle.loads(foodData)
        print('使用redis fD缓存数据')
    else:
        foodData = read_csv('./wordcount/DataForWordCloud/FoodTotal.csv')
        redis_client.set('foodData', pickle.dumps(foodData))
        redis_client.persist('foodData')
        print('没有缓存fD数据，载入redis')
    
    return render_template('index.html',
                           username=username,
                           shopname_maxcomment=shopname_maxcomment,
                           allcomment_count=allcomment_count,
                           active_region=active_region,
                           goodCommentCount=goodCommentCount,
                           middleCommentCount=middleCommentCount,
                           badCommentCount=badCommentCount,
                           sentiment_counts=sentiment_counts,
                           sh_json=sh_json,
                           sr_json=sr_json,
                           foodData=foodData
                           )

@pb.route('/hotWord')
def hotWord():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

    # 热词列表
    cached_data = redis_client.get('hotWordList')
    if cached_data:
        hotWordList=pickle.loads(cached_data)
        print('使用redis hWL缓存数据')
    else:
        hotWordList=getAllHotWord()
        redis_client.set('hotWordList',pickle.dumps(hotWordList))
        redis_client.persist('hotWordList')
        print('没有缓存hWL数据，载入redis')
    
    # 取得默认热词，第一个
    defaultHotWord=hotWordList[0][0]

    # 返回默认热词给网页
    if request.args.get('hotWord'):
        defaultHotWord=request.args.get('hotWord')

    # 取得热词出现的次数
    hotWordLen=getHotWordLen(defaultHotWord)

    hot_word_cache_key = f'hot_word_chart_data:{defaultHotWord}'
    hot_word_chart_data = redis_client.get(hot_word_cache_key)
    if hot_word_chart_data:
        xData, yData = pickle.loads(hot_word_chart_data)
        print('使用redis xy缓存数据')
    else:
        xData, yData = getHotWordChartData(defaultHotWord)
        redis_client.set(hot_word_cache_key, pickle.dumps((xData, yData)))
        redis_client.persist(hot_word_cache_key)
        print('没有缓存xy数据，载入redis')

    sentences=''
    value=SnowNLP(defaultHotWord).sentiments
    if value==0.5:
        sentences='中性'
    elif value > 0.5:
        sentences='积极'
    elif value < 0.5:
        sentences='消极'

    comments = getHotWordCommentData(defaultHotWord)
    
    return render_template('hotWord.html',
                           username=username,
                           hotWordList=hotWordList,
                           defaultHotWord=defaultHotWord,
                           hotWordLen=hotWordLen,
                           sentences=sentences,
                           xData=xData,
                           yData=yData,
                           comments=comments
                           )

@pb.route('/sentimentData0')
def sentimentData0():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

    # 尝试从Redis缓存中获取数据
    cached_data = redis_client.get('sentiment_data_0')
    if cached_data:
        # 如果缓存中有数据，直接使用缓存的数据
        tableData = pickle.loads(cached_data)
        print('使用redis sd0缓存数据')
    else:
        # 如果缓存中没有数据，则查询数据库，并将结果存入Redis缓存
        sql = """
            select userComment,sentiment from all_reviews where sentiment=0 and userName != '匿名用户'
        """
        commentList = myquery(sql, [], 'select')
        tableData = commentList

        # 将查询结果存入Redis缓存，调用persist()方法使其永不过期
        redis_client.set('sentiment_data_0', pickle.dumps(tableData))
        redis_client.persist('sentiment_data_0')
        print('没有缓存sd0数据，载入redis')

    return render_template('sentimentData0.html',
                           username=username,
                           tableData=tableData
                           )



@pb.route('/sentimentData1')
def sentimentData1():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

     # 尝试从Redis缓存中获取数据
    cached_data = redis_client.get('sentiment_data_1')
    if cached_data:
        # 如果缓存中有数据，直接使用缓存的数据
        tableData = pickle.loads(cached_data)
        print('使用redis sd1缓存数据')
    else:
        # 如果缓存中没有数据，则查询数据库，并将结果存入Redis缓存
        sql = """
            select userComment,sentiment from all_reviews where sentiment=1 and userName != '匿名用户'
        """
        commentList = myquery(sql, [], 'select')
        tableData = commentList

        redis_client.set('sentiment_data_1', pickle.dumps(tableData))
        redis_client.persist('sentiment_data_1')
        print('没有缓存sd1数据，载入redis')

    return render_template('sentimentData1.html',
                           username=username,
                           tableData=tableData
                           )

@pb.route('/sentimentData2')
def sentimentData2():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

     # 尝试从Redis缓存中获取数据
    cached_data = redis_client.get('sentiment_data_2')
    if cached_data:
        # 如果缓存中有数据，直接使用缓存的数据
        tableData = pickle.loads(cached_data)
        print('使用redis sd2缓存数据')
    else:
        # 如果缓存中没有数据，则查询数据库，并将结果存入Redis缓存
        sql = """
            select userComment,sentiment from all_reviews where sentiment=2 and userName != '匿名用户'
        """
        commentList = myquery(sql, [], 'select')
        tableData = commentList

        redis_client.set('sentiment_data_2', pickle.dumps(tableData))
        redis_client.persist('sentiment_data_2')
        print('没有缓存sd2数据，载入redis')

    return render_template('sentimentData2.html',
                           username=username,
                           tableData=tableData
                           )



def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            row = [entry.strip('()') for entry in row]
            if len(row) == 2:
                keyword, count = row[0], int(row[1])
                data.append({'name': keyword, 'value': count})
    return data


@pb.route('/cloud')
def cloud():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

    data1=redis_client.get('G2')
    if data1:
        data1=pickle.loads(data1)
        print('使用redis data1缓存数据')
    else:
        data1=read_csv('./wordcount/DataForWordCloud/G2Total.csv')
        redis_client.set('G2',pickle.dumps(data1))
        redis_client.persist('G2')
        print('没有缓存data1数据，载入redis')

    data2=redis_client.get('M2')
    if data2:
        data2=pickle.loads(data2)
        print('使用redis data2缓存数据')
    else:
        data2=read_csv('./wordcount/DataForWordCloud/M2Total.csv')
        redis_client.set('M2',pickle.dumps(data2))
        redis_client.persist('M2')
        print('没有缓存data2数据，载入redis')

    data3=redis_client.get('B2')
    if data3:
        data3=pickle.loads(data3)
        print('使用redis data3缓存数据')
    else:
        data3=read_csv('./wordcount/DataForWordCloud/B2Total.csv')
        redis_client.set('B2',pickle.dumps(data3))
        redis_client.persist('B2')
        print('没有缓存data3数据，载入redis')

    return render_template('cloud.html',
                           username=username,
                           data1=data1,
                           data2=data2,
                           data3=data3
                           )

@pb.route('map')
def map():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

    with open('./data/GZ.json', 'r', encoding='utf-8') as f:
        gz_map_json_data = f.read()

    mapGoodDataSQL='''
        SELECT l.shopRegion as '行政区', COUNT(r.sentiment) AS '好评数'
        FROM all_reviews AS r
        JOIN location AS l ON r.shopName = l.shopName
        WHERE r.sentiment = 0
        GROUP BY l.shopRegion;
    '''
    mapGoodDataList = mapquery(mapGoodDataSQL)
    mapGoodData=[]
    for i in mapGoodDataList:
        mapGoodData.append(i)
    mapGoodData = [{'name': item[0], 'value': item[1]} for item in mapGoodData]

    mapBadDataSQL='''
        SELECT l.shopRegion as '行政区', COUNT(r.sentiment) AS '差评数'
        FROM all_reviews AS r
        JOIN location AS l ON r.shopName = l.shopName
        WHERE r.sentiment = 2
        GROUP BY l.shopRegion;
    '''
    mapBadDataList = mapquery(mapBadDataSQL)
    mapBadData=[]
    for i in mapBadDataList:
        mapBadData.append(i)
    mapBadData = [{'name': item[0], 'value': item[1]} for item in mapBadData]

    return render_template('map.html',
                           username=username,
                           gz_map_json_data=gz_map_json_data,
                           mapGoodData=mapGoodData,
                           mapBadData=mapBadData)




@pb.route('/chat')
def chat():
    # 当前登录账号右上角显示
    if 'username' not in session:
        return redirect('/user/login')
    username = session.get('username')

    # 这里可以根据预测结果进行相应的操作，比如返回给前端
    return render_template('chat.html',
                           username=username)

# @pb.route('/chatchat', methods=['POST'])
# def chatchat():
#     # 获取表单提交的消息
#     data = request.json
#     text = data['text']
#     print("MESSAGE:", text)

#     # 调用模型进行预测
#     sentiment_response=predict_sentiment(text)
#     print(sentiment_response)
#     return jsonify(sentiment_response)


