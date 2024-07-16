# -*- coding: utf-8 -*-
"""
author:Lin
"""
import asyncio
import aiohttp
from loguru import logger
from proxypool.schemas import Proxy
from proxypool.storages.redis import RedisClient
from proxypool.setting import TEST_TIMEOUT, TEST_BATCH, TEST_URL, TEST_VALID_STATUS, TEST_ANONYMOUS, \
    TEST_DONT_SET_MAX_SCORE
from aiohttp import ClientProxyConnectionError, ServerDisconnectedError, ClientOSError, ClientHttpProxyError
from asyncio import TimeoutError

#错误类型合集
EXCEPTIONS = (
    ClientProxyConnectionError,
    ConnectionRefusedError,
    TimeoutError,
    ServerDisconnectedError,
    ClientOSError,
    ClientHttpProxyError,
    AssertionError
)


class Tester(object):
    """
    tester for testing proxies in queue
    """

    def __init__(self):
        """
        init redis
        """
        self.redis = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy: Proxy):
        """
        test single proxy
        :param proxy: Proxy object
        :return:
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                logger.debug(f'正在测试 {proxy.string()}')
                # if TEST_ANONYMOUS is True, make sure that
                # the proxy has the effect of hiding the real IP
                if TEST_ANONYMOUS:
                    url = 'https://httpbin.org/ip'
                    async with session.get(url, timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        origin_ip = resp_json['origin']
                    async with session.get(url, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT) as response:
                        resp_json = await response.json()
                        anonymous_ip = resp_json['origin']
                    assert origin_ip != anonymous_ip
                    assert proxy.host == anonymous_ip
                async with session.get(TEST_URL, proxy=f'http://{proxy.string()}', timeout=TEST_TIMEOUT,
                                       allow_redirects=False) as response:
                    if response.status in TEST_VALID_STATUS:
                        if TEST_DONT_SET_MAX_SCORE:
                            logger.debug(f'代理 {proxy.string()} 有效, 保持近期分数')
                        else:
                            self.redis.max(proxy)
                            logger.debug(f'代理 {proxy.string()} 有效, 最高分数')
                    else:
                        self.redis.decrease(proxy)
                        logger.debug(f'代理 {proxy.string()} 无效, 降低分数')
            except EXCEPTIONS:
                self.redis.decrease(proxy)
                logger.debug(f'代理 {proxy.string()} 无效, 降低分数')

    @logger.catch
    def run(self):
        """
        test main method
        :return:
        """
        # event loop of aiohttp
        logger.info('正在启动tester')
        count = self.redis.count()
        logger.debug(f'{count} 个代理ip需要被测试')
        cursor = 0
        while True:
            logger.debug(f'正在测试代理， 使用游标 {cursor}, 数量 {TEST_BATCH}')
            cursor, proxies = self.redis.batch(cursor, count=TEST_BATCH)
            if proxies:
                tasks = [self.loop.create_task(self.test(proxy)) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break


def run_tester():
    host = '96.113.165.182'
    port = '3128'
    tasks = [tester.test(Proxy(host=host, port=port))]
    tester.loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    tester = Tester()
    tester.run()

