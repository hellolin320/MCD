# -*- coding: utf-8 -*-
"""
author:Lin
需要填写自己的cookie
region_url根据网站进行推测
"""
import csv
import random
import time
import requests
import os

from fake_useragent import UserAgent
from lxml import etree

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def detail_page(detail_url, headers):
    # 发送请求
    rep_detail = requests.get(detail_url, headers=headers)

    # 解析详情页面
    html_tree = etree.HTML(rep_detail.text)

    # 提取ul
    li_list = html_tree.xpath("//div[@id='shop-all-list']/ul/li")
    for li in li_list:
        shopName = ''.join(
            li.xpath("./div[@class='txt']/div[@class='tit']/a/h4/text()"))

        region = ''.join(
            html_tree.xpath("/html/body/div[2]/div[1]/span[4]/a/span//text()")).strip()

        location = ''.join(
            li.xpath("./div[@class='txt']/div[@class='tag-addr']/a[2]//text()")).strip()

        location_info = {
            'shopName': shopName,
            'shopRegion': region,
            'shopLocation': location
        }

        write_to_csv(os.path.join(base_dir, '/data/raw/location.csv'), fieldnames, location_info)

        print('已写入：', region, '---', shopName, '---', location)

    return location_info


def write_to_csv(file_path,fieldnames,data):
    with open(file_path,mode='a',encoding='utf-8',newline='') as f:
        csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
        csv_writer.writerow(data)

if __name__ == '__main__':

    region_url = "c413"
    max_page = 1

    current_page = 1

    # 表头
    fieldnames = [
        'shopName',
        'shopRegion',
        'shopLocation'
    ]

    # 如果没文件，写入表头
    if not os.path.isfile(os.path.join(base_dir, 'data/raw/location.csv')):
        with open(os.path.join(base_dir, 'data/raw/location.csv'), mode='a', encoding='utf-8', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
            csv_writer.writeheader()

    # headers
    headers = {
        "Cookie": "",
        "User-Agent": str(UserAgent().random)
    }

    # main
    for i in range(current_page, max_page+1):
        sleep_time = random.uniform(3, 5)
        time.sleep(sleep_time)
        herf = f"https://www.dianping.com/search/keyword/4/0_%E9%BA%A6%E5%BD%93%E5%8A%B3/{region_url}p{i}"
        location_info = detail_page(herf, headers)
        print("第", i, "页完成", herf)
    print("------OK------")



