import pymysql

# conn1 = pymysql.connect(host='10.10.21.52', port=3306, db='', user='root', passwd='123', charset='utf8')
conn1 = pymysql.connect(host='10.10.11.199', port=3306, db='', user='root', passwd='5bd99b5036', charset='utf8')
cur1 = conn1.cursor()

cur1.execute("SELECT a.DcCode,b.SalesOrderUuid,b.PlanSortNumBasic,b.ReceiveSortNumBasic "+
"FROM joinwms_sorttask.sorttask a "+
"JOIN joinwms_sorttask.sorttaskdetail b ON a.Id = b.Mid "+
"JOIN joinfsc_sales.sales c ON c.Uuid = b.SalesOrderUuid AND c.ReceiverName = '船厂-沙县档口' and c.CustomerUuid = 'd9ea8ebf-5be9-4553-911c-6aa50f1fd0fe' "+
"JOIN joinfsc_sales.salesdetail d ON c.Id = d.Mid AND b.SalesDetailsId = d.Id AND d.ProductName LIKE '%%' "+
"WHERE DATE(a.PlanTime) = '2022-07-25' AND CASE WHEN '' = '' THEN TRUE ELSE a.DcCode IN ('GH02') END AND a.BcCode = 'CN0003';")




results1 = cur1.fetchall()
# results2 = cur2.fetchall()
# results3 = cur3.fetchall()
# results4 = cur4.fetchall()
# for r in rs:
print(results1)
# print(results2)
# print(results3)
# print(results4)
