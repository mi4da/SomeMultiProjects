import requests
from bs4 import BeautifulSoup
import time
from SQL import database
from Regter import *
from concurrent.futures import ThreadPoolExecutor
import random

def spider(url, headers):
    success = False
    while not success:
        try:
            res = requests.get(url, headers=headers)
            success = True
        except:
            num = time.sleep(random.randint(5,20))
            print("糟糕,你的爬虫被发现了！！但是别担心，{}秒后我们就会重启！嘿嘿".format(num))
    # requests默认的编码是‘ISO-8859-1’，会出现乱码，这里重编码为utf-8
    res.encoding = 'utf-8'
    return res.text


def pagemade(text):  # 获取页数列表
    soup = BeautifulSoup(text, 'html.parser')
    reslis = soup.find_all('a', target="_blank")[3:-4:2]  # 固定的序列分割模式
    reslis = [i['href'] for i in reslis]
    return reslis


def save(file_name, text):
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(str(text) + '\n')


def contentmade(content_text):
    content_soup = BeautifulSoup(content_text, 'html.parser')

    # try:

    title = content_soup.find_all("td",
                                  style="FONT-WEIGHT: bold;FONT-SIZE: 14pt;COLOR: #d52b2b;LINE-HEIGHT: 250%;FONT-FAMILY: 宋体;TEXT-ALIGN: center")[
        0].text.strip()

    # 对于文本的选择content_soup.find_all("p")[4:-4]

    invitation = get_invitor(content_text)
    win = get_win(content_text)
    money = get_money(content_text)
    win_time = get_date(content_text)
    sql_lis = ["中标文件", invitation, win, win_time, money, title, content_text]
    # except:
    #     sql_lis = ["中标文件", "", "", "", "", "", content_text]
    return sql_lis


def sign_main(page_url):
    # 定义头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    # 定义拼接字符串
    content_url = "http://www.shangluo.gov.cn"
    # 获得页面数据
    pagetext = spider(page_url, headers)
    # 获得页面链接列表
    page_list = pagemade(pagetext)
    # 内容循环
    for j in page_list:
        # 获得内容数据
        content_text = spider(content_url + j, headers)
        # 获得内容实体列表
        content_list = contentmade(content_text)
    return content_list


def get_all_content_url(url):
    # 定义头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    # 定义拼接字符串
    content_url = "http://www.shangluo.gov.cn"
    # 获得页面数据
    try:
        pagetext = spider(page_url, headers)
    except:
        time.sleep()
    # 获得页面链接列表
    page_list = pagemade(pagetext)
    return page_list


def get_obj_list(url):
    # 定义头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    content_text = spider(url, headers)
    # 获得内容实体列表
    content_list = contentmade(content_text)
    return content_list


if __name__ == '__main__':
    # 爬取历史数据
    # 打开数据库连接
    info = {
        "host": "localhost",
        "user": "root",
        "password": "haizeiwang",
        "db": "TESTDB",
        "charset": "utf8"  # 一定要加上负责中文无法显示
    }

    db = database(info)
    # 创建数据表，如果存在则删除
    db.create_table()
    st = time.time()
    # 定义原始页面url
    page_url = "http://www.shangluo.gov.cn/zwgk/szfgkmlxxgk.jsp?ainfolist1501t=24&ainfolist1501p={}&ainfolist1501c=15&urltype=egovinfo.EgovInfoList&subtype=2&wbtreeid=1232&sccode=zccg_zhbgg&gilevel=2"
    # 定义拼接字符串
    content_url = "http://www.shangluo.gov.cn"

    """并行方案: 用两遍多线程，一遍获得所有的url，一遍过得所有的实体列表"""
    # 生成所有页面url
    urls = [page_url.format(i) for i in range(1, 25)]
    """开启页面线程池子"""
    executer = ThreadPoolExecutor(max_workers=8)
    # 生成map对象
    concent_concurrent_url_list = executer.map(get_all_content_url, urls)
    # 实例化map对象,获得所有内容url
    _concent_concurrent_url_list_maped = list(concent_concurrent_url_list)
    # 将列表展开
    concent_concurrent_url_list_maped = []
    for j in _concent_concurrent_url_list_maped:
        for k in j:
            concent_concurrent_url_list_maped.append(content_url + k)

    # # ---阻塞---
    print("页面线程已全部结束，进入10秒睡眠")
    time.sleep(10)
    print("睡眠结束，进入内容线程阶段")

    # 生成map对象
    obj_concurrent_list = executer.map(get_obj_list, concent_concurrent_url_list_maped)
    # 实例化map对象，获得所有实体列表
    obj_concurrent_list_maped = list(obj_concurrent_list)

    # 将列表展开并保存
    count = 0
    for i in obj_concurrent_list_maped:
        # save("./Current_content_list.txt", i)
        # 将实体列表保存进数据库
        db.insert_data(i)
        print("第{}条数据插入完毕".format(count))
        count += 1
    et = time.time()
    print("并行用时：", (et - st))
