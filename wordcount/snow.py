# -*- coding: utf-8 -*-
"""
author:Lin
调用 SnowNLP, 将情感写入每条评论
"""

from snownlp import SnowNLP
import csv
import os
from cutComments import getAllCommentData
def targetFile():
    targetFile='target.csv'
    commentList=getAllCommentData()

    rateData=[]
    good=0
    bad=0
    middle=0

    for index,i in enumerate(commentList):
        value=SnowNLP(i[6]).sentiments
        if value>0.5:
            good+=1
            rateData.append([i[6],'积极'])
        elif value==0.5:
            middle+=1
            rateData.append([i[6],'中性'])
        elif value<0.5:
            bad+=1
            rateData.append([i[6],'消极'])

    # for i in rateData:
    #     with open(targetFile,'a+',encoding='utf8',newline='') as f:
    #         writer=csv.writer(f)
    #         writer.writerow(i)

    # 一次性将所有数据写入文件
    with open(targetFile,'a+',encoding='utf8',newline='') as f:
        writer=csv.writer(f)
        writer.writerows(rateData)

def main():
    targetFile()

if __name__ == '__main__':
    main()