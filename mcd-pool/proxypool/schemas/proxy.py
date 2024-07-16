# -*- coding: utf-8 -*-
"""
author:Lin
"""
from attr import attrs, attr

@attrs
class Proxy(object):
    """
    代理元数据
    """
    host = attr(type=str, default=None)
    port = attr(type=int, default=None)

    def __str__(self):
        """
        输出
        :return:
        """
        return f'{self.host}:{self.port}'

    def string(self):
        """
        变成字符串
        :return: <host>:<port>
        """
        return self.__str__()


if __name__ == '__main__':
    proxy = Proxy(host='8.8.8.8', port=8888)
    print('proxy', proxy)
    print('proxy', proxy.string())
