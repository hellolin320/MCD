# -*- coding: utf-8 -*-
"""
author:Lin
"""
import requests
from lxml import html
import time
import random

from spiders.get_proxy import get_proxy
from spiders.get_useragent import get_useragent


# 实际的起始和结束页数
start_page = 1
end_page = 26

with open('href.txt', 'w', encoding='utf-8') as file:
    # 循环遍历每一页
    for page in range(start_page, end_page + 1):

        # 构造当前页面的URL
        url = f'https://www.dianping.com/search/keyword/4/0_%E9%BA%A6%E5%BD%93%E5%8A%B3/p{page}'

        proxies = {
            'http':'http://'+str(get_proxy()),
            'https': 'https://' + str(get_proxy())
        }
        headers = {
            'Cookie': '',
            'Host': 'www.dianping.com',
            'Referer': 'https://www.dianping.com/search/keyword/4/0_%E9%BA%A6%E5%BD%93%E5%8A%B3',
            'User-Agent': str(get_useragent())
        }
        print("ip:", proxies)
        print("头文件:", get_useragent())

        # 发送请求获取页面内容
        response = requests.get(url=url, headers=headers,proxies=proxies)
        print('第', page, '页的链接')
        file.write(f'第 {page} 页的连接：\n')

        # 使用lxml的html模块创建一个XPath解析器
        tree = html.fromstring(response.text)

        # 使用XPath选择所有li元素
        li_elements = tree.xpath('//*[@id="shop-all-list"]/ul/li')

        # 遍历每个li元素，并提取链接
        for li_element in li_elements:

            # 使用相对XPath选择器提取链接
            shop_link = li_element.xpath('.//div[@class="pic"]/a/@href')

            # 打印链接
            print(shop_link)

            # 写入链接到文件
            file.write(str(shop_link)+ '\n')
        # 生成随机睡眠时间，模拟人的操作行为
        sleep_time = random.uniform(3.9, 6)  # 设置睡眠时间范围
        time.sleep(sleep_time)
print('已写入')


