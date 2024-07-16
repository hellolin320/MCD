# -*- coding: utf-8 -*-
"""
author:Lin
将食物进行分词，并保存为txt
"""
import re
import time
from collections import Counter
from utils.myquery import myquery
import jieba


def stopWordList():
    mcdWords=[line.strip() for line in open('../data/mcd.txt',encoding='utf8').readlines()]
    stopwordslist=mcdWords
    return stopwordslist

def seg_depart(sentence):
    valid_sentences = [x[3] for x in sentence if x[3] is not None]
    sentence_depart = jieba.cut(" ".join(valid_sentences).strip())
    stopWords = stopWordList()
    outStr = ''
    for word in sentence_depart:
        if word not in stopWords:
            if word != '\t':
                outStr += word
    return outStr


def getFoodData(targetTxt):
    foodList=myquery('select * from all_reviews where sentiment=0',[],'select')
    with open(targetTxt,'a+',encoding='utf-8') as targetFile:
        seg=jieba.cut(seg_depart(foodList),cut_all=True)
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
    FoodTxt='DataForWordCloud/Food.txt'
    getFoodData(FoodTxt)

    FoodTotal='DataForWordCloud/FoodTotal.csv'
    total(FoodTxt,FoodTotal)