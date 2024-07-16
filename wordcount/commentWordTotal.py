# -*- coding: utf-8 -*-
"""
author:Lin
将评论进行分词，并保存为txt
"""
import time
from collections import Counter
import jieba
import re

from utils.myquery import myquery
from wordcount.cutComments import seg_depart, writer_comments_cuts

def getGoodCommentData(targetTxt):
    GcommentList=myquery('select * from all_reviews where sentiment=0',[],'select')
    with open(targetTxt,'a+',encoding='utf-8') as targetFile:
        seg=jieba.cut(seg_depart(GcommentList),cut_all=True)
        output=' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
        print('成功写入',targetTxt)

def getMiddleCommentData(targetTxt):
    McommentList=myquery('select * from all_reviews where sentiment=1',[],'select')
    with open(targetTxt,'a+',encoding='utf-8') as targetFile:
        seg=jieba.cut(seg_depart(McommentList),cut_all=True)
        output=' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
        print('成功写入',targetTxt)

def getBadCommentData(targetTxt):
    BcommentList=myquery('select * from all_reviews where sentiment=2',[],'select')
    with open(targetTxt,'a+',encoding='utf-8') as targetFile:
        seg=jieba.cut(seg_depart(BcommentList),cut_all=True)
        output=' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
        print('成功写入',targetTxt)


def total(txt,csv):
    start_time=time.time()
    print('START_TIME',start_time)

    reader=open(txt,'r',encoding='utf8')
    start=reader.read()
    print('READING ',txt)
    result=open(csv,'w',encoding='utf-8')
    print('WRITING ',csv)

    word_list=jieba.cut(start,cut_all=True)
    print('Jieba Cutting')

    new_words=[]
    print('RE start')
    for i in word_list:
        m=re.search("\d+",i)
        n=re.search("\W+",i)
        if not m and not n and len(i)>1:
            new_words.append(i)
    print('RE over')

    # word_count={}
    # for i in set(new_words):
    #     word_count[i]=new_words.count(i)
    #
    # list_count=sorted(word_count.items(),key=lambda x:x[1],reverse=True)
    # print('降序排序over')
    #
    # print('Writing File...')
    # for i in range(100):
    #     print(list_count[i],file=result)

    # 使用 Counter 统计单词出现次数
    word_count = Counter(new_words)

    # 将统计结果转换为按出现次数降序排列的列表
    list_count = word_count.most_common()

    # 只保留前 200 个结果
    list_count = list_count[:200]

    # 将结果写入文件
    for word, count in list_count:
        result.write(f"({word},{count})\n")

    end_time=time.time()
    run_time=end_time-start_time
    print('计算时长',run_time)
if __name__ == '__main__':
    G1Txt='../wordcount/DataForWordCloud/G1.txt'
    M1Txt='../wordcount/DataForWordCloud/M1.txt'
    B1Txt='../wordcount/DataForWordCloud/B1.txt'
    getGoodCommentData(G1Txt)
    getMiddleCommentData(M1Txt)
    getBadCommentData(B1Txt)

    G2Total='../wordcount/DataForWordCloud/G2Total.csv'
    M2Total='../wordcount/DataForWordCloud/M2Total.csv'
    B2Total='../wordcount/DataForWordCloud/B2Total.csv'
    total(G1Txt,G2Total)
    total(M1Txt,M2Total)
    total(B1Txt,B2Total)