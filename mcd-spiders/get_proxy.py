# -*- coding: utf-8 -*-
"""
author:Lin
"""
import requests

PROXY_POOL_URL = 'http://192.168.137.160:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


