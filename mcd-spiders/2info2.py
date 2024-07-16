# -*- coding: utf-8 -*-
"""
author:Lin
需要填写自己的cookie
"""
import requests
import re
import time
import random
import csv
import os
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

def get_shop_info(url,headers):

    # 发送请求
    response = requests.get(url=url, headers=headers)

    # 解析详情页面
    shop_detail = etree.HTML(response.text)

    # 提取店名
    shop_name=''.join(
        shop_detail.xpath("/html/body/div/div[2]/div[2]/div[1]/div[1]/h1/text()"))

    # 提取综合评分
    star_score=''.join(
        shop_detail.xpath("//div[@class='star_score score_40']/text()")).strip(' ')

    # 口味
    taste_score1=''.join(
        shop_detail.xpath("//div[@id='review-list']/div[2]/div[1]/div[2]/span[3]/span[1]/text()")).strip(' ')
    taste_score2 = re.search(r'\d+.\d+', taste_score1)
    if taste_score2:
        taste_score = taste_score2.group()
    else:
        taste_score=" "

    # 环境
    env_score1=''.join(
        shop_detail.xpath("//div[@id='review-list']/div[2]/div[1]/div[2]/span[3]/span[2]/text()")).strip(' ')
    env_score2 = re.search(r'\d+.\d+', env_score1)
    if env_score2:
        env_score = env_score2.group()
    else:
        env_score=" "

    # 服务
    ser_score1=''.join(
        shop_detail.xpath("//div[@id='review-list']/div[2]/div[1]/div[2]/span[3]/span[3]/text()")).strip(' ')
    ser_score2 = re.search(r'\d+.\d+', ser_score1)
    if ser_score2:
        ser_score = ser_score2.group()
    else:
        ser_score=" "

    # 好评数量
    good_count1=''.join(
        shop_detail.xpath("//label[@class='filter-item filter-good']/span[@class='count']/text()")).strip(' ')
    good_count2 = re.search(r'\d+', good_count1)
    if good_count2:
        good_count = good_count2.group()
    else:
        good_count=0

    # 中评数量
    middle_count1=''.join(
        shop_detail.xpath("//label[@class='filter-item filter-middle']/span[@class='count']/text()")).strip(' ')
    middle_count2 = re.search(r'\d+', middle_count1)
    if middle_count2:
        middle_count = middle_count2.group()
    else:
        middle_count=0

    # 差评数量
    bad_count1=''.join(
        shop_detail.xpath("//label[@class='filter-item filter-bad']/span[@class='count']/text()")).strip(' ')
    bad_count2 = re.search(r'\d+', bad_count1)
    if bad_count2:
        bad_count = bad_count2.group()
    else:
        bad_count=0


    print("爬取写入:",shop_name)
    print("综合评分:",star_score)
    print("口味评分:",taste_score)
    print("环境评分:",env_score)
    print("服务评分:",ser_score)
    print("好评数量:",good_count)
    print("中评数量:",middle_count)
    print("差评数量:",bad_count)

    shop_info = {
        'shopName': shop_name,
        'starScore': star_score,
        'tasteScore': taste_score,
        'envScore':env_score,
        'serScore':ser_score,
        'goodCount':good_count,
        'middleCount':middle_count,
        'badCount':bad_count
    }
    write_to_csv(os.path.join(base_dir, '/data/raw/info2.csv'), fieldnames, shop_info)
    return shop_info

def write_to_csv(file_path,fieldnames,data):
    with open(file_path,mode='a',encoding='utf-8',newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writerow(data)

if __name__ == '__main__':
    fieldnames = [
        'shopName',
        'starScore',
        'tasteScore',
        'envScore',
        'serScore',
        'goodCount',
        'middleCount',
        'badCount'
    ]

    raw_data_dir = os.path.join(base_dir, 'data/raw')
    os.makedirs(raw_data_dir, exist_ok=True)

    if not os.path.isfile(os.path.join(base_dir, 'data/raw/info2.csv')):
        with open(os.path.join(base_dir, 'data/raw/info2.csv'), mode='a', encoding='utf-8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()
    headers = {
        'Cookie': '',
        'User-Agent': str(UserAgent().random)
    }

    #门店
    start_shop_url=2
    list=open_txt_start_index(start_shop_url-1)

    for shop in list:
        sleep_time = random.uniform(1,7)
        time.sleep(sleep_time)
        shop_url=f"{shop}/review_all"
        shop_info = get_shop_info(shop_url, headers)
        print("^^^",shop)



