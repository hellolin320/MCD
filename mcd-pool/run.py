# -*- coding: utf-8 -*-
"""
author:Lin
"""
from proxypool.scheduler import Scheduler
import argparse

parser = argparse.ArgumentParser(description='ProxyPool')
parser.add_argument('--processor', type=str, help='processor to run')
args = parser.parse_args()

if __name__ == '__main__':
    # if processor set, just run it
    if args.processor:
        getattr(Scheduler(), f'运行_{args.processor}')()
    else:
        Scheduler().run()