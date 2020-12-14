import requests
import threading
from threading import Thread
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor

"""爬取一部小说的全部章节"""


class SerialSpyder:
    def __init__(self, url):
        self.url = url
        self.index = 0

    def set_index(self, i):
        self.index = i

    def get_list(self):
        response = requests.get(self.url)

    def regux_list(self):
        pass

    def save_list(self, filename):
        pass


class ConcurrentSpyder:
    pass


if __name__ == '__main__':
    url = "https://www.biquge.lol/book/1983/index_{}.html"
    """串行爬取"""
    sspyder = SerialSpyder(url)
    #  爬取前64叶
    for i in range(1, 65):
        # 设置页码
        sspyder.set_index(i)
        # 获得章节列表
        sspyder.get_list()
        # 正则化章节列表
        sspyder.regux_list()
        # 保存章节列表
        sspyder.save_list(filename="三寸人间")

    """并行爬取"""
    cspyder = ConcurrentSpyder()
