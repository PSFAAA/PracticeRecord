import openpyxl
import pymysql

# 创建工作簿对象
workbook = openpyxl.Workbook()
# 获得默认的工作表
sheet = workbook.active
# 修改工作表的标题
sheet.title = '部门基本信息'
# 给工作表添加表头
sheet.append(('部门编号', '部门名称', '部门所在地'))
# 创建连接（Connection）
conn = pymysql.connect(host='10.10.11.81', port=3306,
                       user='sa', password='5bd99b5036',
                       database='join_fsc_ns1', charset='utf8')
try:
    # 获取游标对象（Cursor）
    with conn.cursor() as cursor:
        # 通过游标对象执行SQL语句
        cursor.execute(
            'select `no`, `name`, `location` from `test_python`'
        )
        # 通过游标抓取数据
        row = cursor.fetchone()
        while row:
            # 将数据逐行写入工作表中
            sheet.append(row)
            row = cursor.fetchone()
    # 保存工作簿
    workbook.save('hrs.xlsx')
except pymysql.MySQLError as err:
    print(err)
finally:
    # 关闭连接释放资源
    conn.close()