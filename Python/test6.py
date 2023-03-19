import pymysql

no = int(input('部门编号: '))
name = input('部门名称: ')
location = input('部门所在地: ')

# 1. 创建连接（Connection）
conn = pymysql.connect(host='10.10.11.81', port=3306,
                       user='sa', password='5bd99b5036',
                       database='join_fsc_ns1', charset='utf8')
try:
    # 2. 获取游标对象（Cursor）
    with conn.cursor() as cursor:
        # 3. 通过游标对象向数据库服务器发出SQL语句
        affected_rows = cursor.execute(
            'insert into `test_python` values (%s, %s, %s)',
            (no, name, location)
        )
        if affected_rows == 1:
            print('新增部门成功!!!')
    # 4. 提交事务（transaction）
    conn.commit()
except pymysql.MySQLError as err:
    # 4. 回滚事务
    conn.rollback()
    print(type(err), err)
finally:
    # 5. 关闭连接释放资源
    conn.close()