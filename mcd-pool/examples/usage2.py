# -*- coding: utf-8 -*-
"""
author:Lin
"""
import requests

'''
输出代理
目标网站
'''
proxypool_url = 'http://127.0.0.1:5555/random'
target_url = 'https://antispider5.scrape.center/'


def get_random_proxy():
    """
    从代理池中得到ip
    :return: proxy
    """
    return requests.get(proxypool_url).text.strip()


def crawl(url, proxy):
    """
    使用ip访问目标网站
    :param url: page url
    :param proxy: proxy, such as 8.8.8.8:8888
    :return: html
    """
    proxies = {'http': 'http://' + proxy}
    return requests.get(url, proxies=proxies).text


def main():
    """
    main method, entry point
    :return: none
    """
    proxy = get_random_proxy()
    print('随机代理：', proxy)
    html = crawl(target_url, proxy)
    print(html)


if __name__ == '__main__':
    main()