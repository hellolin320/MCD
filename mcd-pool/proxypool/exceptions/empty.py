# -*- coding: utf-8 -*-
"""
author:Lin
"""
class PoolEmptyException(Exception):
    def __str__(self):
        """
        空
        :return:
        """
        return repr('代理池中没有IP')
