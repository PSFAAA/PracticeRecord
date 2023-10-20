import os
import re
import pymysql
import datetime

today = datetime.date.today()
fileDir = os.getcwd()

def listFiles(dirPath):
    # 遍历指定文件夹下当天的sql文件
    fileList = []

    for root, dirs, files in os.walk(dirPath):

        for fileObj in files:
            filePath = os.path.join(root, fileObj)
            if os.path.splitext(fileObj)[1] == ".sql":
                # fileList.append(filePath)
                # 获取文件的最后修改时间
                modification_time = os.path.getmtime(filePath)
                modification_date = datetime.date.fromtimestamp(modification_time)
                if modification_date == today:
                    fileList.append(filePath)

    return fileList


def execute_fromfile(filename, cursor):
    file_name = filename.split('/')[-1]
    fd = open(filename, 'r', encoding='utf-8')
    sqlfile = fd.read()
    fd.close()
    sqlcommamds = sqlfile.split(';')[0:-1]

    for command in sqlcommamds:
        try:
            cursor.execute(command)
        except Exception as e:
            print("message:", e)

    print(file_name,'执行完成')


def connect_mysql():
    # 建立连接
    conn = pymysql.connect(host='10.10.21.200', port=3306, user='root', password='jx_123', db='joindbv_api')
    print(conn.host,"数据库连接成功")
    # 获取游标对象
    cursor = conn.cursor()

    for filename in listFiles(fileDir):
        execute_fromfile(filename, cursor)

    # 关闭连接
    conn.close()


if __name__ == '__main__':
    connect_mysql()



