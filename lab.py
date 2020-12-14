####-*-encoding:utf8-*-
"""
author:yy zhou
time:2020.11.24
目标爬取网站整本小说
"""


import requests as rq
import re
import time


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
    #print("ht:", ht)
    title = re.findall(r'<h1 class="title">(.+)</h1>',ht)
    #print("title:",title)
    content = re.findall(r'<br \/>(.+)<script language=',ht)
    data_content = clean(content[0])
    return title[0]+"&&"+data_content



def main():
    #page_urls = get_url(3324998,3329148)
    page_urls = get_url(3324998, 3326000)
    page = []
    for page_url in page_urls:
        #print("page_url:",page_url)
        #url1 = page_url[2]
        #url1 = "https://www.biquge.lol/book/9118/3329148_2.html"
        try:
            title_content = get_data(page_url)
            page.append(title_content)
        except:
            page.append("")
            continue
    with open("E:/北理珠/工作/2020下半年/并行与分布式计算/cap7/lab/xxx.txt","w",encoding="utf8") as f:
        f.write("\n".join(page))

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("总共花费时间：{}".format(end - start))



