import requests
import threading
from threading import Thread
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import re
from bs4 import BeautifulSoup

"""爬取一部小说的全部章节"""


class SerialSpyder:
    def get_url(self, url):
        self.url = url

    def get_text(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
        self.response = requests.get(self.url, headers)

    def regux_list(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        content_list = []
        for tag in soup.find_all("ul", class_="section-list fix"):
            # 对tag的子节点进行循环输出
            for child in tag.children:
                # print(child)
                # 将对象存进数组
                content_list.append(child)
        # 获取中间的20个的内容
        return [obj.string for obj in content_list[14:-1]]

    def save_list(self, filename, lis):
        with open(filename, 'a') as f:
            for i in range(len(lis)):
                f.write(lis[i]+'\n')
        print("保存结束")

class ConcurrentSpyder:
    pass


if __name__ == '__main__':
    url = "https://www.biquge.lol/book/1983/index_{}.html"

    """串行爬取"""
    start = time.time()
    sspyder = SerialSpyder()
    #  爬取前64叶
    for i in range(1, 65):
        # 设置url
        format_url = url.format(i)
        # 设置页码
        sspyder.get_url(format_url)
        # 获得章节列表
        sspyder.get_text()
        # 正则化章节列表
        lis = sspyder.regux_list()
        # 保存章节列表
        sspyder.save_list(filename="./三寸人间.txt", lis=lis)
        print("第{}轮结束".format(i))
    end = time.time()
    print("串行耗时：",(end-start))

    """并行爬取"""
    cspyder = ConcurrentSpyder()
