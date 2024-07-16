# -*- coding: utf-8 -*-
"""
author:Lin
"""
from fake_useragent import UserAgent

def get_useragent():
    # 获取随机 User-Agent
    ua = UserAgent()
    return ua.random


