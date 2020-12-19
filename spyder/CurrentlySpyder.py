import requests
import threading
from threading import Thread
import time
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import re
from bs4 import BeautifulSoup


def save_list(filename, lis):
    with open(filename, 'a+') as f:
        for i in lis:
            for j in i:
                f.write(j + '\n')
    print("保存结束")

def CurrentForData(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    respones = requests.get(url,headers)

    """正则化"""
    soup = BeautifulSoup(respones.text,'html.parser')
    content_list = []
    for tag in soup.find_all("ul", class_="section-list fix"):
        # 对tag的子节点进行循环输出
        for child in tag.children:
            print(child)
            # 将对象存进数组
            content_list.append(child)
    return [obj.string for obj in content_list[14:-1]]


if __name__ == '__main__':
    """使用线程池并行爬取小说标题"""

    """构造url"""
    url = "https://www.biquge.lol/book/1983/index_{}.html"
    urls = [url.format(i) for i in range(1, 5)]

    """开启线程池子"""
    executer = ThreadPoolExecutor(max_workers=4)

    """并行爬取"""
    # 生成map对象
    concurrent_list = executer.map(CurrentForData, urls)
    # 实例化map对象
    concurrent_list_maped = list(concurrent_list)

    """保存"""
    save_list("./current_三寸人间.txt",concurrent_list_maped)
