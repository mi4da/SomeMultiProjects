import requests
from bs4 import BeautifulSoup
import time
from SQL import database


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


def save(name, text):
    with open("./{}.html".format(name), 'w') as f:
        f.write(text)


def contentmade(content_text):
    content_soup = BeautifulSoup(content_text, 'html.parser')
    title = content_soup.find_all("td",
                                  style="FONT-WEIGHT: bold;FONT-SIZE: 14pt;COLOR: #d52b2b;LINE-HEIGHT: 250%;FONT-FAMILY: 宋体;TEXT-ALIGN: center")[
        0].text.strip()
    # 只要“结果公告、结果公示”
    """
        文件类型 CHAR(50) NOT NULL,
        招标方  CHAR(20) NOT NULL,
        中标方  CHAR(20) NULL,   
        成交时间 DATE NULL,
        成交金额 INT NULL,
        文件标题 CHAR(50) NULL,
        文件内容 LONGTEXT NULL,
    """
    if ("结果公告" or "结果公示") in title:
        # 对于文本的选择content_soup.find_all("p")[4:-4]
        text = content_soup.find_all("p")[4:-4]
        invitation = text[16].text
        win = text[4].text
        win_time = text[-1].text  # 还需要进一步处理
        win_time = win_time.replace("年", "-")
        win_time = win_time.replace("月", "-")
        win_time = win_time.replace("日", "-")
        money = text[6].text
        sql_lis = ["中标文件", invitation, win, win_time, money, title, content_text]
    else:
        sql_lis = ["中标文件", "", "", "", "", title, content_text]

    return sql_lis


if __name__ == '__main__':
    # 爬取历史数据
    # 链接数据库
    info = {
        "host": "localhost",
        "user": "root",
        "password": "Haizeiwang_123",
        "db": "GOVDB",  # 记得提前创建数据库
        "charset": "utf8"  # 一定要加上负责中文无法显示
    }
    db = database(info)
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
    for i in range(1, 24):
        # 获得页面数据
        pagetext = spider(page_url.format(i), headers)
        # 获得页面链接列表
        page_list = pagemade(pagetext)
        # 内容循环
        for j in page_list:
            # 获得内容数据
            content_text = spider(content_url + j, headers)
            # 获得内容实体列表
            content_list = contentmade(content_text)
            # 将实体列表保存进数据库
            db.insert_data(content_list)
