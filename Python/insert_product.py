import json
import requests
import base64
import decimal
import operator
import re
import sys

from itertools import groupby

import pymysql
from itertools import chain
from pypinyin import pinyin, Style
from decimal import Decimal
from datetime import datetime, timedelta

# region Help-Method[MySQL]
def connect():
    conn = pymysql.connect(**ConnConfig)
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
Result = {"main":{"Id":-4,"Name":"素菜","Type":"Custom","DayNum":1,"EndTime":"18:00","Remark":""},"products":[],"customers":[],"receivers":[]}
Tablelist = []

def fetch_tablelist():
    global Tablelist
    sql_t = (
        "SELECT Uuid FROM `t01-v001`.product WHERE Name IN {0};"
        ).format(ProductNames)

    Tablelist = fetchall(sql_t)

def build_data():
    tableList = list(list(items) for items in list(Tablelist))
    tableData = []
    No = 1
    if tableList is not None:
        for ttl in tableList:
            prodate = {}
            data = json.loads(json.dumps(prodate))
            data['Id'] = -No
            data['ProductUuid'] = ttl[0]
            # prodate = json.dumps(data, ensure_ascii=False)
            No+=1
            tableData.append(data)
    result = tableData
    return result


def request_post(url, param):
    fails = 0
    while True:
        try:
            if fails >= 20:
                break

            headers = {"authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiMTJmN2NkMy02ZDA2LTQyNjgtYTFhZi1hY2QyNjJmZGZjZjYiLCJuYW1lIjoi5ZC05aec5Y2aIiwianRpIjoiNjE0ZTlmZDAtNzliNi00NmYwLTllM2MtZDcwMGRmMjU3M2JhIiwiY29kZSI6IjE1MDIxNjg4MjA2IiwidHV1aWQiOiI3ODY0M2VlMi03OTA4LTQ3ZjMtYmJjMi05ZjFkM2I4ZDgwNzciLCJ0bmFtZSI6IuWNl-S6rOiNo-mCpumkkOmlriIsInRjb2RlIjoiVklQMjAyMzA1MDAwMSIsInRmbGFnIjoiTlJCIiwiaXNzYSI6IkZhbHNlIiwiaXNhZG1pbiI6IkZhbHNlIiwiZXhwIjoxNjkyMDg2MzYwLCJpc3MiOiJhY2NvdW50LmpvaW52MyIsImF1ZCI6ImpvaW52MyJ9.fHSXmzAzwcmFMSPp71w5_CEmfPhv3k-E2kXllxSZRNs",
                 "jt-bc": "CN0004", "content-type": "application/json"}
            ret = requests.post(url, json=param, headers=headers, timeout=10)

            if ret.status_code == 200:
                text = json.loads(ret.text)
            else:
                continue
        except:
            fails += 1
            print('网络连接出现问题, 正在尝试再次请求: ', fails)
        else:
            break
    return text

if __name__ == '__main__':
    global ProductNames,ConnConfig
    ProductNames =   "('韭菜','韭黄','荷兰芹','西芹','侉芹','水芹','香芹','药芹','菜秧','上海青','大白菜','矮脚黄（青菜）','紫生菜','有机花菜','龙须菜（盒）','芥菜','油麦菜','小白菜','广东菜心','秧草','娃娃菜（袋）','榴榴菜','穿心莲','冰草','木耳菜','平包菜','香菜','空心菜','苋菜','菠菜','生菜','马兰头','洋兰','紫菜苔','青菜苔','荠菜','西兰花','蒲菜','紫包菜','包菜','圆茄子（青）','长茄子（紫）','水海带','水发海带丝','青南瓜','黄瓜','小黄瓜','日本南瓜','南瓜','冬瓜','丝瓜','地瓜','菜瓜','净茭瓜','毛茭瓜','佛手瓜','苦瓜','广东节瓜','笋瓜','金瓜','鲜百合（袋）','春笋','冬笋','乌饭叶','莴笋','芦笋','水笋（馒头笋）','藕','芥兰','茼蒿','鲜带壳花生','鲜菱角米','菱角','蚕豆瓣','带壳毛豆','新鲜毛豆米','青扁豆','红扁豆','小土豆','土豆','豇豆','荷兰豆','四季豆','黄豆芽','甜豆','刀豆','蒜仔','带皮蒜头','黑蒜（袋）','青蒜','蒜苗','蒜黄','京葱','干葱头','洋葱','香葱','大葱','生姜','蘑菇','杏鲍菇','秀珍菇','草菇','姬菇','茶树菇','金针菇','鲜香菇','海鲜菇','百灵菇','白玉菇','蟹味菇','鲜玉米棒','山芋','紫薯','马蹄','球生菜','鲜板栗仁','带壳板栗','瓠子','香芋','芋苗','山芋梗','黄瓜苗','萝卜苗','花生苗','铁棍山药','山药','小黄胡萝卜','杨花萝卜','心里美(水果萝卜)','胡萝卜','青萝卜','白萝卜','西红柿','黄彩椒','红彩椒','红杭椒','青杭椒','薄皮青椒','红椒','青椒','鲜小米辣','小甘兰','绿茸菜','皇帝菜','养心菜','甘蓝菜','四季红','核桃花','伏郎','南瓜藤','雪樱子','桔梗','石参','鲜玉竹','麒麟菜','观音菜','芝麻菜','羽衣甘蓝','樱桃番茄','番杏','紫苏叶','鲜粽叶（袋）','罗勤叶','冬寒草','明日草','鲜香茅草','紫贝天葵','鲜虫草','塔塔菜','苦菊','菊叶','冬葵','秋葵','鲜莲子','莲蓬','景天三七','白背三七','皮腊','梅干菜','小油面筋','大油面筋（袋）','酸豇豆','清水笋丝（箱）','青雪菜','雪菜','腌菜','酱黄瓜（袋）','碎雪菜（袋）','黑大头菜（袋）','酸豇豆碎（袋）','干海带','红油豆角（箱）','辣妹子榨菜丝（箱）','老坛萝卜干（箱）','榨菜（箱）','榨菜丝（箱）','海带丝（箱）','海带花（箱）','海带结（箱）','笋片（箱）','青圆椒','裙带菜（箱）','水笋（桶）','生姜片（袋）','彭州酸菜（箱）','东北酸菜（箱）','鲜虫草花','新鲜南姜','螺丝菜','鲜鸡枞菌','新鲜雪里红','绣球菌','黑豆芽','溧阳白芹','全形雪菜','贡菜','碳烤笋','红菜头','广东丝瓜','全形雪里红','泡椒罗汉笋','小南瓜','小杂菇','罗汉笋箱装','新鲜去壳银杏','荠菜花','清水笋丁（箱）','新鲜粽叶KG','新鲜荷叶','苦百合','豆皮','花玉米棒','薄荷叶KG','鲜木耳','马齿苋','韭苔','香椿苗（盒）','条纹萝卜','鲜茴香','黑糖蒜头','情人草（束）','小黄豆芽','五仁酱丁','酸模叶','三色堇','千叶吊兰','干地皮菜（袋）','鲜银耳','枸杞头','蒲公英','新蒜','葫芦','长寿菜','干马齿苋','贵族南瓜','网纹草','鲜金耳','姬松茸（盒）','鸡腿菇（袋）','龙爪菇','玉女黄瓜','牛心包菜','鲜竹花','鲜牛肝菌','鲜竹荪KG','冰鲜牛肝菌','冰鲜松茸（袋）','小香薯','林清酸菜（箱）','灰树花KG','矮脚青','马家沟芹菜','小冬瓜（个）','黄金玫瑰','扁尖笋（箱）','贝贝南瓜','章丘鲍芹','陈小二萝卜干','黄金柳芽','鹿茸菌（箱）','芥兰苗','嫩生姜','大娃娃菜')"

    jConn = '{"host":"rm-uf6a3z1ci9lom9e897o.mysql.rds.aliyuncs.com","port":3306,"user":"v3sa","passwd":"Kq4d6RbP","db":""}'
    ConnConfig = json.loads(jConn)
    url = "https://rbcy.freshcloud.link/b010/api/v1/GoodsTemplate/save"
    fetch_tablelist()
    Result["products"] = build_data()
    request_post(url, Result)


