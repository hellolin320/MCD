# -*- coding: utf-8 -*-
"""
author:Lin
"""
import csv
import os
import random
import re
import time
import requests
import get_proxy
from lxml import etree
from fake_useragent import UserAgent

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 读取链接
def open_txt_start_index(start_index):
    with open('href.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # start_index =   # 第五行的索引为4
        content = lines[start_index:]

        list = []
        for index,match in enumerate(content,start=start_index):
            match = re.search(r'https://www\.dianping\.com/shop/\S+', match)
            if match:
                links = match.group().rstrip("']")
                list.append(links)
    return list

# 获取评论数据
def detail_page(detail_url,headers,proxies):
    # 发送请求
    rep_detail = requests.get(detail_url, headers=headers,proxies=proxies)

    # 解析详情页面
    page_detail = etree.HTML(rep_detail.text)

    # 提取评论ul
    comment_li_list = page_detail.xpath("//div[@class='reviews-items']/ul/li")
    if comment_li_list:
        # 提取评论数据
        for comment_li in comment_li_list:
            # 获取店铺名
            shopName = ''.join(
                page_detail.xpath("//div[@class='review-shop-wrap']//h1[@class='shop-name']/text()"))

            # 用户名
            userName = ''.join(
                comment_li.xpath("./div[@class='main-review']/div[@class='dper-info']//text()")).strip()

            #推荐的菜品
            recommendFood = ' '.join(
                comment_li.xpath("./div[@class='main-review']/div[@class='review-recommend']/a[@class='col-exp']//text()"))

            # 用户评论时间
            userCommentTime = ''.join(
                comment_li.xpath("./div[@class='main-review']//span[@class='time']/text()")).strip()

            # 用户评分
            userScore1 = comment_li.xpath("./div[@class='main-review']/div[@class='review-rank']/span[@class='score']/span[@class='item'][1]/text()")
            if userScore1:
                userScore2=userScore1[0].strip()
                userScore3=re.search(r'\d+\.\d+', userScore2)
                userScore=userScore3.group(0)
            else:
                userScore=" "

            # 用户评论
            userComment = ''.join(
                comment_li.xpath("./div[@class='main-review']/div[@class='review-words']/text()")).strip()
            if not userComment:
                userComment=''.join(comment_li.xpath("./div[@class='main-review']/div[@class='review-words Hide']/text()")).strip()

            comment_info = {
                'shopName': shopName,
                'userName': userName,
                'recommendFood': recommendFood,
                'userCommentTime': userCommentTime,
                'userScore': userScore,
                'userComment': userComment
            }

    else:
        # 获取店铺名
        shopName = ''.join(
            page_detail.xpath("//div[@class='review-shop-wrap']//h1[@class='shop-name']/text()"))
        comment_info = {
            'shopName': shopName
        }
    write_to_csv(os.path.join(base_dir, '/data/raw/bad.csv', fieldnames, comment_info))
    return comment_info


def get_page(detail_url,headers):
    # 向更多评论页面发送请求
    rep_detail = requests.get(detail_url, headers=headers)

    # 解析详情页面
    page_detail = etree.HTML(rep_detail.text)

    # 提取页码列表,提取最大页码
    page_list = page_detail.xpath("//div[@class='bottom-area clearfix']")
    for page in page_list:
        # 最大页码
        p = page.xpath("./div[@class='reviews-pages']//text()")
        if p:
            p = p[-4].strip(', ')
        else:
            p=1
    return p

def write_to_csv(file_path,fieldnames,data):
    with open(file_path,mode='a',encoding='utf-8',newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writerow(data)

if __name__ == "__main__":
    fieldnames = [
        'shopName',
        'userName',
        'recommendFood',
        'userCommentTime',
        'userScore',
        'userComment'
    ]

    raw_data_dir = os.path.join(base_dir, 'data/raw')
    os.makedirs(raw_data_dir, exist_ok=True)


    if not os.path.isfile(os.path.join(base_dir, 'data/raw/bad.csv')):
        with open(os.path.join(base_dir, 'data/raw/bad.csv'), mode='a', encoding='utf-8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()

    proxies = {
        "http": "http://"+str(get_proxy())
    }
    headers = {
        "Cookie":"",
        "User-Agent": str(UserAgent().random)
    }

    start_shop_url=2
    current_page = 1
    list=open_txt_start_index(start_shop_url-1)

    for shop in list:
        sleep_time = random.uniform(10,20)
        time.sleep(sleep_time)
        shop_url=f"{shop}/review_all?queryType=reviewGrade&queryVal=bad"
        p=int(get_page(shop_url,headers))+1
        print("最大页数=",p-1)
        for i in range(current_page,p):
            sleep_time=random.uniform(40,50)
            time.sleep(sleep_time)
            herf=f"{shop_url}/p{i}?queryType=reviewGrade&queryVal=bad"
            comment_info = detail_page(herf, headers,proxies)
            print("第",i,"页完成",shop)
