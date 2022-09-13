# This is a sample Python script.
import decimal
import json
import operator
import re
import sys

from itertools import groupby

import pymysql
from itertools import chain
from pypinyin import pinyin, Style


# region Help-Class
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o == 0:
                return 0
            return float(o)
        super(DecimalEncoder, self).default(o)


# endregion

def to_pinyin(s):
    return ''.join(chain.from_iterable(pinyin(s, style=Style.TONE3)))


# region Help-Method[MySQL]
def connect():
    conn = pymysql.connect(**ConnConfig)
    # conn = pymysql.connect(host="10.10.11.81", port=3306, user="sa", passwd="5bd99b5036", db="join_fsc_ms1")
    return conn


def fetchone(sql):
    conn = connect()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(e)


def fetchall(sql):
    conn = connect()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


# endregion

# region Help-Method
def concat(t):
    t = tuple(t) if type(t) != tuple else t
    t = [str(de) for de in t]
    result = ",".join(t)
    return result


def tolist(t):
    t = ",".join(t) if type(t) == tuple or type(t) == list else t
    t = str(t) if type(t) != str else t
    result = t.split(",")
    result = [de for de in result if de != '']
    return result


def first(target, d=None):
    result = target[0] if len(target) > 0 else d
    return result


# endregion

# region $A.常量
# endregion

# region A.成员变量
ConnConfig = {"host": "10.10.11.81", "port": 3306, "user": "sa", "passwd": "5bd99b5036", "db": "join_fsc_ms1"}
Variable = {"ID": 1, "CID": 2, "SEQ": 1}
RUQUIRE_DATE: str
CUSTOMER: str
CID: int
SEQ: int
Result = {
    "success": False, "message": "未知错误",
    "data": {
        "x": [],
    }
}

CateGoryIO = None  # None 为所有时使用 IN 或 NOT IN
CateGroup = []
CateGory = ""
CustomerIds = []
Orders = []
InCustomerIds = []


# endregion


# region X.成员方法[category]
def fetch_category_group():
    global CateGoryIO, CateGroup

    sql = ("SELECT SEQ, NAME, VALUE "
           "FROM d_datadict "
           "WHERE IS_DELETE=0 AND CID={0} "
           "AND CATEGORY='DDProductCategoryGroup' "
           "ORDER BY SEQ;").format(CID)
    cate_groups = fetchall(sql)
    cate = [de for de in cate_groups if de[0] == SEQ]
    cate = first(cate)
    if cate is not None:
        if cate[2] != "ALL" and cate[2] != "-":
            CateGoryIO = "IN"
            CateGroup = tolist(cate[2])
        elif cate[2] == "-":
            CateGoryIO = "NOT IN"
            CateGroup = [de[2] for de in cate_groups if de[2] != "ALL" and de[2] != "-"]
            CateGroup = tolist(CateGroup)
        elif cate[2] == "ALL":
            CateGoryIO = None
            CateGroup = [tolist(de[2]) for de in cate_groups]
    return CateGroup


def fetch_category():
    global CateGory
    if CateGoryIO is not None:
        sql = ("SELECT KID "
               "FROM b_product_category "
               "WHERE IS_DELETE=0 AND CID={0}"
               " AND (PARENT_ID IN ({1}) OR KID IN ({1}));").format(CID, concat(CateGroup))
        category_sql = fetchall(sql)
        CateGory = [de[0] for de in category_sql]
    return CateGory


# endregion

# region X.成员方法[InventorySum]
def fetch_customer_ids():
    global InCustomerIds
    if CUSTOMER != '':
        InCustomerIds = [CUSTOMER]
    else:
        sql = ("SELECT DISTINCT(CUSTOMER_ID) "
               "FROM b_sales_order "
               "WHERE CID={0} AND IS_DELETE=0 AND "
               " STATUS <> 'Obsoleted' AND"
               " SUBSTRING(RUQUIRE_TIME,1,10) = '{1}' ").format(CID, RUQUIRE_DATE)

        data = fetchall(sql)
        InCustomerIds = [de[0] for de in data]

    return InCustomerIds


# endregion

# region X.成员方法[b_sales_order]
def fetch_b_sales_order():
    global Orders
    if CateGoryIO is not None:
        sql_product_type = " AND d.PRODUCT_TYPE {0} ({1}) ".format(CateGoryIO, concat(CateGory))
    else:
        sql_product_type = " "

    sql_r = ("SELECT "
             "dict.NAME DICT_NAME, "
             "catep.NAME CATEGORY_PARENT_NAME, "
             "cate.NAME CATEGORY_NAME, "
             "d.PRODUCT_ID, "
             "d.PRODUCT_NAME, "
             "d.ORDER_UNIT, "
             "SUM(d.ORDER_ORDERS) ORDER_RECEIPTNUM, "
             "0 ORDER_RECEIPTNUMS, "
             "m.CUSTOMER_ID "
             "FROM b_sales_order m "
             "JOIN b_sales_order_xdetail d "
             "ON d.PID=m.KID "
             "AND d.IS_DELETE=0 {0}"

             "JOIN b_product_category cate "
             "ON d.PRODUCT_TYPE = cate.KID "
             "AND cate.IS_DELETE=0 "
             "AND cate.CID={1} "

             "LEFT JOIN b_product_category catep "
             "ON cate.PARENT_ID = catep.KID "
             "AND catep.IS_DELETE=0 "
             "AND catep.CID={1} "

             "JOIN d_datadict dict "
             "ON dict.CATEGORY='DDProductCategoryGroup'"
             "AND (FIND_IN_SET(cate.KID,dict.VALUE) OR FIND_IN_SET(cate.PARENT_ID,dict.VALUE))"
             "AND dict.IS_DELETE=0 "
             "AND dict.CID={1} "

             "WHERE m.IS_DELETE=0 AND m.CID={1} AND "
             "m.STATUS <> 'Obsoleted' AND "
             "SUBSTRING(m.RUQUIRE_TIME,1,10)='{2}' AND "
             "m.CUSTOMER_ID IN ({3}) "
             "GROUP BY d.PRODUCT_ID,m.CUSTOMER_ID"
             ).format(sql_product_type, CID, RUQUIRE_DATE, concat(InCustomerIds))

    sql_l = ("SELECT cust.KID, cust.CUSTOMER_NAME  "
             "FROM d_customer cust "
             "WHERE cust.IS_DELETE=0 "
             "AND cust.CID={0} "
             "AND cust.KID IN ({1})").format(CID, concat(InCustomerIds))

#  "IF(r.CATEGORY_PARENT_NAME is NULL, '', CONCAT(r.CATEGORY_PARENT_NAME, '|')) CATEGORY_PARENT_NAME, "

    sql = ("SELECT "
           "r.DICT_NAME, "
           "IF(r.CATEGORY_PARENT_NAME is NULL, '', r.CATEGORY_PARENT_NAME) CATEGORY_PARENT_NAME, "
           "r.CATEGORY_NAME, "
           "r.PRODUCT_NAME, "
           "r.ORDER_UNIT, "
           "CASE WHEN r.CUSTOMER_ID = l.KID THEN r.ORDER_RECEIPTNUM ELSE 0 END ORDER_RECEIPTNUM, "
           "CASE WHEN r.CUSTOMER_ID = l.KID THEN r.ORDER_RECEIPTNUMS ELSE 0 END ORDER_RECEIPTNUMS, "
           "l.CUSTOMER_NAME "
           "FROM ({0}) l INNER JOIN ({1}) r ON r.CUSTOMER_ID = l.KID;").format(sql_l, sql_r)

    Orders = fetchall(sql)


# endregion

def build_b_sales_order():
    ordersList = list(Orders)

    # ordersList['sum'] = ordersList.groupby(['PRODUCT_NAME'])['ORDER_RECEIPTNUMS'].sum()

    data = []

    for i, g in groupby(sorted(ordersList), key=lambda x: x[0] + '' + x[1] + '' + x[2] + '' + x[3]):
        gv = tuple(g)
        sumNum = sum(v[5] for v in gv)
        for glv in gv:
            glvl = list(glv)
            data.append((glvl[0],
                         glvl[1],
                         glvl[3],
                         glvl[4],
                         glvl[5],
                         sumNum,
                         glvl[7]))

    dataList = list(data)

    dataList.sort(key=lambda de: to_pinyin(de[6]))
    dataList.sort(key=lambda de: to_pinyin(de[3]))
    dataList.sort(key=lambda de: to_pinyin(de[2]))
    dataList.sort(key=lambda de: to_pinyin(de[1]))
    dataList.sort(key=lambda de: to_pinyin(de[0]))

    result = [dict(zip(
        ["DICT_NAME",
         "CATEGORY_NAME",
         "PRODUCT_NAME",
         "ORDER_UNIT",
         "ORDER_RECEIPTNUM",
         "ORDER_RECEIPTNUMS",
         "CUSTOMER_NAME"
         ], v)) for v in dataList]

    return result


# region M.主体方法
def _():
    try:
        fetch_category_group()
        fetch_category()
        fetch_customer_ids()
        fetch_b_sales_order()

        Result["data"]["x"] = build_b_sales_order()

    except Exception as e:
        _end(str(e))
    else:
        _end()


# endregion

# region L.加载方法
def _begin(argv):
    if len(argv) < 3:
        _end("缺少参数")

    _db(argv[1])
    _variable(argv[2])
    _()


def _db(s):
    values = re.split("&|=", s)
    global ConnConfig
    ConnConfig = dict(zip(values[0::2], values[1::2]))
    ConnConfig["port"] = int(ConnConfig["port"])


def _variable(s):
    values = re.split("&|=", s)
    global Variable, CID, SEQ, RUQUIRE_DATE, CUSTOMER
    Variable = dict(zip(values[0::2], values[1::2]))
    RUQUIRE_DATE = Variable["RUQUIRE_DATE"]
    CUSTOMER = Variable["CUSTOMER"]
    CID = int(Variable["CID"])
    SEQ = int(Variable["SEQ"])


def _end(msg=None):
    if msg is not None:
        Result["message"] = msg
    else:
        Result["success"] = True
        del Result["message"]
    print(json.dumps(Result, cls=DecimalEncoder, ensure_ascii=False))
    sys.exit()


# endregion

# region K.构造方法
if __name__ == '__main__':
    _begin(sys.argv)
# endregion
