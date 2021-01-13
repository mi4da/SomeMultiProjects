import regex as re


# 获得招标方，关键词："采购单位：...\n","采购人信息\n名 称：...\n","采购人名称：...\n"
def get_invitor(data):
    pattern_list = ["(?s)<P>1.采购人信息</P>\r\n<P>名 称：(.*?)</P>", '采购单位：(.*)</p>', "采购人名称：(.*)</P>"]
    for i in pattern_list:
        res = re.findall(i, data)
        if res:
            invator = res[0]
            break  # 只要第一个条件满足就行
        else:
            invator = ""
    return invator


# 获得中标方,关键词："中标单位：...\n","中标方：...\n","中标供应商：...\n","供应商名称："
def get_win(data):
    pattern_list = ['供应商名称：(.*)</P>', "中标单位：(.*)</P>", "中标方：(.*)</P>"]
    for i in pattern_list:
        if re.findall(i, data):
            win = re.findall(i, data)[0]
            break  # 只要第一个条件满足就行
        else:
            win = ""
    return win


# 获得成交金额，关键词："成交金额：...\n","中标金额：...\n","中标价：\n"
def get_money(data):
    pattern_list = ['成交金额：(.*)</P>', "中标金额：(.*)</P>", "中标价：(.*)<\P>"]
    for i in pattern_list:
        if re.findall(i, data):
            money = re.findall(i, data)[0]
            break  # 只要第一个条件满足就行
        else:
            money = ""
    return money


# 获得成交时间,正则匹配第一次的时间，之后还要转换sql格式
def get_date(data):
    time = re.findall("(\d{4}年\d{1,2}月\d{1,2}日)", data)[0]
    time = time.replace("年", "-").replace("月", '-').replace("日", "")
    return time

if __name__ == '__main__':
    with open("./testdir/content.html", 'r', encoding='utf-8') as f:
        data = f.read()
    import requests

    page_url = "http://www.shangluo.gov.cn/zwgk/szfgkmlxxgk.jsp?ainfolist1501t=24&ainfolist1501p=1&ainfolist1501c=15&urltype=egovinfo.EgovInfoList&subtype=2&wbtreeid=1232&sccode=zccg_zhbgg&gilevel=2"
    content_url = "http://www.shangluo.gov.cn" + "/info/egovinfo/zwgk/zwgk-nry/01606072-9-30/2020-1117005.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    res = requests.get(content_url, headers=headers)
    # requests默认的编码是‘ISO-8859-1’，会出现乱码，这里重编码为utf-8
    res.encoding = 'utf-8'
    # print(data)
    """
                文件类型 CHAR(50) NOT NULL,
                招标方  CHAR(20) NOT NULL,
                中标方  CHAR(20) NULL,   
                成交时间 DATE NULL,
                成交金额 INT NULL,
                文件标题 CHAR(50) NULL,
                文件内容 LONGTEXT NULL,
            """
    test = """<span property="v:summary">
                                    　　《2001太空漫游》后9年，前国家航天委员会主任弗洛伊德博士（罗伊•谢德 Roy Scheider 饰）接受苏美合作计划，带领发现号航天站设计者科脑博士（约翰•利思戈 John Lithgow 饰）和HAL9000电脑的创始人钱德拉博士（鲍勃•巴拉班 Bob Balaban 饰）登录木星附近的苏联航空站，与苏联宇航员卡布珂（海伦•米伦 Helen Mirren 饰）等合作，空中接轨美国发现号航天站，调查九年前的事故原因，探索木卫二的神秘黑石，并查明宇航员大卫•伯曼（凯尔•杜拉 Keir Dullea 饰）缘何神秘失踪。然而任务执行尚未过半，美苏关系愈发紧张，战争一触即发；与此同时，大卫•伯曼竟突然现身对弗洛伊德博士发出神秘警告。
                                        <br>
                                    　　本片改编自亚瑟•克拉克的小说《2010太空漫游》，获第59界奥斯卡最佳艺术指导—布景，最佳服装设计，最佳视觉效果，最佳化妆...
                            </span>
"""
    print(re.findall("(?s)<span.*property=\"v:summary\">(.*?)</span>",test))
    print(re.findall("(?s)<P>1.采购人信息</P>\r\n<P>名 称：(.*?)</P>",res.text))
    # print(get_invitor(res.text))