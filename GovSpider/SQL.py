import pymysql


class database:
    def __init__(self, info=None):
        if info != None:
            self.info = info
        else:
            self.info = {
                "host": "localhost",
                "user": "root",
                "password": "Haizeiwang_123",
                "db": "TESTDB",
                "charset": "utf8"  # 一定要加上负责中文无法显示
            }

    def create_table(self):

        # 打开数据库链接
        db = pymysql.connect(**self.info)
        # 创建游标对象
        cursor = db.cursor()
        # 使用 execute() 方法执行 SQL，如果表存在则删除
        cursor.execute("DROP TABLE IF EXISTS 商洛市政府官网中标信息")

        # 使用预处理语句创建表
        sql = """CREATE TABLE 商洛市政府官网中标信息 (
        id INT AUTO_INCREMENT,
        文件类型 CHAR(50) NOT NULL,
        招标方  CHAR(20) NULL,
        中标方  CHAR(20) NULL,   
        成交时间 DATE NULL,
        成交金额 INT NULL,
        文件标题 CHAR(50) NULL,
        网页内容 LONGTEXT NULL,
        PRIMARY KEY ( `id` )
        )"""
        cursor.execute(sql)

        # 关闭数据库连接
        db.close()

    def insert_data(self, content=None):
        # 链接数据库
        db = pymysql.connect(**self.info)
        # 创建游标对象
        cursor = db.cursor()
        # SQL 插入语句
        sql = "INSERT INTO 商洛市政府官网中标信息(文件类型, \
               招标方, 中标方, 成交时间, 成交金额, 文件标题, 网页内容) \
               VALUES ('%s', '%s',  '%s',  '%s',  '%d', '%s', '%s')" % \
              (content)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()

        # 关闭数据库连接
        db.close()


if __name__ == '__main__':
    db = database()
    db.create_table()
    db.insert_data()
