import requests
from bs4 import BeautifulSoup
import time
from SQL import database
from Regter import *
import sys
def spider(url, headers):
    res = requests.get(url, headers=headers)
    # requests默认的编码是‘ISO-8859-1’，会出现乱码，这里重编码为utf-8
    res.encoding = 'utf-8'
    return res.text


def pagemade(text):  # 获取页数列表
    soup = BeautifulSoup(text, 'html.parser')
    reslis = soup.find_all('a', target="_blank")[3:-4:2]  # 固定的序列分割模式
    reslis = [i['href'] for i in reslis]
    return reslis


def save(file_name, text):
    with open(file_name, 'a',encoding='utf-8') as f:
        f.write(str(text)+'\n')


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

def main(m,n=None):
    if n == None:
        n = m // 15 + 1# 保证比总条数多一页
    else:
        pass

    # 爬取更新书数据
    # 链接数据库
    db = database()
    # 创建数据表
    db.create_table()
    # 定义原始页面url
    page_url = "http://www.shangluo.gov.cn/zwgk/szfgkmlxxgk.jsp?ainfolist1501t=24&ainfolist1501p={}&ainfolist1501c=15&urltype=egovinfo.EgovInfoList&subtype=2&wbtreeid=1232&sccode=zccg_zhbgg&gilevel=2"
    # 定义拼接字符串
    content_url = "http://www.shangluo.gov.cn"
    # 定义头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    # 页面循环
    for i in range(1, n):
        # 获得页面数据
        pagetext = spider(page_url.format(i), headers)
        # 获得页面链接列表
        page_list = pagemade(pagetext)
        # 内容循环
        for j in page_list[:m]:
            # 获得内容数据
            content_text = spider(content_url + j, headers)
            # 获得内容实体列表
            content_list = contentmade(content_text)
            # 将实体列表保存进数据库
            db.insert_data(content_list)
            # 将实体列表保存
            # save("./update_content_list.txt",content_list)
        print('第{}页爬取完毕'.format(i))

if __name__ == '__main__':
    m = eval(input("请指定爬取条数："))
    try:
        n = eval(input("请指定爬取页数（可以为空）："))
    except:
        n = None

    main(m,n)


