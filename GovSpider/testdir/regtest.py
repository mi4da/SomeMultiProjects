import re
with open("content.html",'r',encoding='utf-8') as f:
    data = f.read()
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
# 获得招标方，关键词："采购单位：...\n","采购人信息\n名 称：...\n","采购人名称：...\n"
test = """\n<P>1.采购人息</P>\n<P>名 称：商洛市市场监督管理局</P>\n<P>采购单位：大大大大jb</p>"""
pattern_list = ['采购人信息</P>\n<P>(.*)</P>','<P>采购单位：(.*)</p>',"<P>采购人名称：(.*)<\p>"]
for i in pattern_list:
    if re.findall(i,data):
        invator = re.findall(i,data)[0]
        break # 只要第一个条件满足就行
    else:
        invator = ""

print(invator)
# invator = re.findall("采购人信息</P>\n<P>(.*)</P>",test)

# 获得中标方,关键词："中标单位：...\n","中标方：...\n","中标供应商：...\n"
# 获得成交金额，关键词："成交金额：...\n","中标金额：...\n","中标价：\n"
# 获得成交时间,正则匹配第一次的时间，之后还要转换sql格式
time = re.findall("(\d{4}年\d{1,2}月\d{1,2}日)",data)[0]
time = time.replace("年","-").replace("月",'-').replace("日","")
print(time)
# 获得文件标题：元素选取。
# 获得文件内容：get请求