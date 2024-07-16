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
        shop_detail.xpath("//h1[@class='shop-name']/text()")).strip(' ')

    # 提取评价条数
    review_count1 = ''.join(
        shop_detail.xpath("//span[@id='reviewCount']/text()")).strip(' ')
    review_count2 = re.search(r'\d+', review_count1)
    review_count = int(review_count2.group())

    # 提取人均消费
    avg_price1 = ''.join(
        shop_detail.xpath("//span[@id='avgPriceTitle']/text()")).strip(' ')
    avg_price2 = re.search(r'\d+', avg_price1)
    if avg_price2:
        avg_price = int(avg_price2.group())
    else:
        avg_price=" "

    # 提取地址信息
    address = ''.join(
        shop_detail.xpath("//span[@id='address']/text()")).strip(' ')

    # 提取电话信息
    tel = ''.join(
        shop_detail.xpath("//p[@class='expand-info tel']/text()")).strip(' ')

    # 提取营业时间
    time=''.join(
        shop_detail.xpath("//p[@class='info info-indent']/span[2]/text()")).strip(' ')

    print("爬取写入:",shop_name)
    print("评论数:",review_count)
    print("人均价格:",avg_price)
    print("地址:",address)
    print("电话:",tel)
    print("营业时间:",time)

    shop_info = {
        'shopName': shop_name,
        'reviewCount': review_count,
        'avgPrice': avg_price,
        'address': address,
        'tel': tel,
        'time': time
    }
    write_to_csv(os.path.join(base_dir, '/data/raw/info1.csv'), fieldnames, shop_info)
    return shop_info

def write_to_csv(file_path,fieldnames,data):
    with open(file_path,mode='a',encoding='utf-8',newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writerow(data)

if __name__ == '__main__':
    fieldnames = [
        'shopName',
        'reviewCount',
        'avgPrice',
        'address',
        'tel',
        'time'
    ]

    raw_data_dir = os.path.join(base_dir, 'data/raw')
    os.makedirs(raw_data_dir, exist_ok=True)

    if not os.path.isfile(os.path.join(base_dir, 'data/raw/info1.csv')):
        with open(os.path.join(base_dir, 'data/raw/info1.csv'), mode='a', encoding='utf-8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()
    headers = {
        'Cookie': '',
        'User-Agent': str(UserAgent().random)
    }


    start_shop_url=2
    list=open_txt_start_index(start_shop_url-1)


    for shop in list:
        sleep_time = random.uniform(1,7)
        time.sleep(sleep_time)
        shop_url=f"{shop}"
        shop_info = get_shop_info(shop_url, headers)
        print("^^^",shop)



