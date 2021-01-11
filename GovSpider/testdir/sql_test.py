import pymysql


class database:
    def __init__(self,info=None):
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
    def create_database(self):

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
        PRIMARY KEY ( `id` )
        )"""
        cursor.execute(sql)

        # 关闭数据库连接
        db.close()

    def insert_data(self,content):
        pass


if __name__ == '__main__':
    db = database()
    db.create_database()
    db.insert_data()
