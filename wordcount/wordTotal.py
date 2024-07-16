# -*- coding: utf-8 -*-
"""
author:Lin
热词计数
"""
import time
from collections import Counter

import jieba
import re

def main():
    start_time=time.time()
    print('START_TIME',start_time)

    reader=open('cutComments.txt','r',encoding='utf8')
    start=reader.read()
    print('READING cutComments.txt')
    result=open('wordTotal.csv','w',encoding='utf-8')
    print('READING wordTotal.txt')

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

    # 只保留前 100 个结果
    list_count = list_count[:100]

    # 将结果写入文件
    for word, count in list_count:
        result.write(f"({word},{count})\n")

    end_time=time.time()
    run_time=end_time-start_time
    print('计算时长',run_time)
if __name__ == '__main__':
    main()