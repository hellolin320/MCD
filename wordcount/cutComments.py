# -*- coding: utf-8 -*-
"""
author:Lin
评论分词处理，为热词wordcount做准备
"""
import jieba
import jieba.analyse as analyse

from utils.myquery import myquery



def getAllCommentData():
    commentList=myquery('select * from all_reviews',[],'select')
    return commentList

def stopWordList():
    stopWords=[line.strip() for line in open('../data/stopwords1.txt',encoding='utf8').readlines()]
    mcdWords=[line.strip() for line in open('../data/mcd.txt',encoding='utf8').readlines()]
    stopwordslist=stopWords+mcdWords
    return stopwordslist

def seg_depart(sentence):
    sentence_depart=jieba.cut(" ".join([x[6] for x in sentence]).strip())
    stopWords=stopWordList()
    outStr=''
    for word in sentence_depart:
        if word not in stopWords:
            if word !='\t':
                outStr+=word
    return outStr

def writer_comments_cuts(targetTxt):
    with open(targetTxt,'a+',encoding='utf-8') as targetFile:
        seg=jieba.cut(seg_depart(getAllCommentData()),cut_all=True)
        output=' '.join(seg)
        targetFile.write(output)
        targetFile.write('\n')
        print('成功写入',targetTxt)

if __name__ == '__main__':
    targetTxt='cutComments.txt'
    writer_comments_cuts(targetTxt)