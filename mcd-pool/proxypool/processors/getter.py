# -*- coding: utf-8 -*-
"""
author:Lin
"""
from loguru import logger
from proxypool.storages.redis import RedisClient
from proxypool.setting import PROXY_NUMBER_MAX
from proxypool.crawlers import __all__ as crawlers_cls


class Getter(object):
    """
    代理池getter
    """

    def __init__(self):
        """
        初始化redis和爬虫
        """
        self.redis = RedisClient()
        self.crawlers_cls = crawlers_cls
        self.crawlers = [crawler_cls() for crawler_cls in self.crawlers_cls]

    def is_full(self):
        """
        代理池未满-False；满-True
        return: bool
        """
        return self.redis.count() >= PROXY_NUMBER_MAX

    @logger.catch
    def run(self):
        """
        日志
        爬取ip保存至redis
        :return:
        """
        if self.is_full():
            return
        for crawler in self.crawlers:
            logger.info(f'爬虫 {crawler} 获取代理')
            for proxy in crawler.crawl():
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
