####-*-encoding:utf8-*-
"""
author:yy zhou
time:2020.11.24
目标并行爬取网站整本小说
"""
import requests as rq
import re
import time
from threading import Thread
import threading
import numpy as np  ####主要用于列表拆分
from concurrent.futures import ThreadPoolExecutor


###############获取整本小说的url的列表
#url = "https://www.biquge.lol/book/9118/{}_{}.html"
#3324997 ~3329148_2
########构建需要爬取小说的url列表
def get_url(num,num1):
    url = []
    #for i in range(3324997,3325000):
    for i in range(num, num1):
        url1 = "https://www.biquge.lol/book/9118/{}.html".format(i)
        url2 = "https://www.biquge.lol/book/9118/{}_{}.html".format(i,2)
        url.append(url1)
        url.append(url2)
    return url

#############清除网页格式
def clean(string):
    pattern = re.compile(r'<[^>]+>', re.S)
    string = pattern.sub('', string)
    string = string.replace('\n', ' ').replace('\r', ' ').replace('&nbsp;', ' ').replace('\t', ' ').replace(" ",'')
    string = string.strip()
    return string


###通过每一页的url爬取小说数据
def get_data(url):
    print("url:",url)
    ht = rq.get(url).text
    time.sleep(1.0)
    #print("ht:", ht)
    title = re.findall(r'<h1 class="title">(.+)</h1>',ht)
    #print("title:",title)
    content = re.findall(r'<br \/>(.+)<script language=',ht)
    data_content = clean(content[0])
    return title[0]+"&&"+data_content


def line_for_data(num_list):
    num2 = num_list[0]
    num3 = num_list[1]
    page_urls = get_url(num2, num3)
    page = []
    for page_url in page_urls:
        try:
            num = page_url.replace("https://www.biquge.lol/book/9118/","").replace(".html","").replace("_",".")
            title_content = get_data(page_url)
            page.append([num,title_content])
        except:
            page.append([num,""])
            continue
    #with open("E:/北理珠/工作/2020下半年/并行与分布式计算/cap7/lab/xxx.txt","w",encoding="utf8") as f:
        #f.write("\n".join(page))
    return page







##################threading并行获取小说#########
######threading
def threading_for_data(num_list):
    num2 = num_list[0]
    num3 = num_list[-1]
    page_urls = get_url(num2, num3)
    page = []
    thread_name = threading.current_thread().name
    for page_url in page_urls:
        try:
            num = page_url.replace("https://www.biquge.lol/book/9118/","").replace(".html","").replace("_",".")
            title_content = get_data(page_url)
            page.append([num,title_content])
        except:
            num = page_url.replace("https://www.biquge.lol/book/9118/", "").replace(".html", "").replace("_", ".")
            page.append([num,""])
            continue
    file = "page"+thread_name+".txt"
    a = open(file,"w",encoding='utf8')
    page_list = [i[1] for i in page]
    page_str = "\n".join(page_list)
    a.write(page_str)
    a.close()

######concurrent
def concurrent_for_data(page_url):
    page = []
    try:
        num = page_url.replace("https://www.biquge.lol/book/9118/","").replace(".html","").replace("_",".")
        title_content = get_data(page_url)
        page.append([num,title_content])
    except:
        page.append([num,""])
    return page

if __name__ == "__main__":
    num = 3324998
    num1 = 3329148
    num10 = 3325010

    ###########串行代码###############
    start = time.time()
    table_and_ficticon = line_for_data([num, num10])
    content_list = [i[1] for i in table_and_ficticon]
    content_str = "\n".join(content_list)
    a = open("line_fiction.txt","w",encoding="utf8")
    a.write(content_str)
    a.close()
    end = time.time()
    print("串行爬取小说花费时间：{}\n".format(end - start))
    print("串行爬取小说每章花费时间：{} s/章(2页)\n".format(((end - start)/(num10-num))))
    #串行爬取小说花费时间：51.056127071380615
    #串行爬取小说每章花费时间：4.254677255948384 s/ 章(2页)

    print("###############串行代码太过缓慢，采用threading的线程并行爬取的方式！#############")
    start1 = time.time()
    ##########################
    table_list = [i for i in range(num,num1)]
    print("list:",list(np.array_split(table_list, 6)[0]))
    p1 = Thread(target=threading_for_data, args=(list(np.array_split(table_list, 6)[0]),))
    p2 = Thread(target=threading_for_data, args=(list(np.array_split(table_list, 6)[1]),))
    p3 = Thread(target=threading_for_data, args=(list(np.array_split(table_list, 6)[2]),))
    p4 = Thread(target=threading_for_data, args=(list(np.array_split(table_list, 6)[3]),))
    p5 = Thread(target=threading_for_data, args=(list(np.array_split(table_list, 6)[4]),))
    p6 = Thread(target=threading_for_data, args=(list(np.array_split(table_list, 6)[5]),))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    end1 = time.time()
    print("threading开启6核并行花费时间：{}\n".format(end1 - start1))
    print("threading开启6核并行爬取小说每章花费时间：{} s/章(2页)\n".format(((end1 - start1) / (num1 - num))))
    ###共3788章threading开启6核并行花费时间：2936.83971118927
    ####threading并行爬取小说每章花费时间：1.289821840058877 s/ 章(2页)

    print("###############串行代码太过缓慢，采用第二种线程——concurrent的并行爬取的方式！#############")
    start2 = time.time()
    page_urls = get_url(num, num1)
    executor = ThreadPoolExecutor(max_workers=12)
    concurrent_table_content = executor.map(concurrent_for_data, page_urls)
    concurrent_table_content_list = list(concurrent_table_content)
    concurrent_table_content_list_new = [i[0][1] for i in concurrent_table_content_list]
    concurrent_content_str = "\n".join(concurrent_table_content_list_new)
    #executor.shutdown()
    c = open("concurrent_fiction.txt","w",encoding='utf8')
    c.write(concurrent_content_str)
    c.close()
    end2 = time.time()
    print("concurrent开启6核并行花费时间：{}\n".format(end2 - start2))
    print("concurrent开启6核并行爬取小说每章花费时间：{} s/章(2页)\n".format(((end2 - start2) / (num1 - num))))
    ###共3788章concurrent开启6核并行花费时间：2901.0010273456573
    ####concurrent并行爬取小说每章花费时间：1.305756185537337 s/ 章(2页)
    #concurrent开启12核并行花费时间：1450.3642182350159
    #concurrent开启12核并行爬取小说每章花费时间：0.3494853537915701 s/章(2页)






