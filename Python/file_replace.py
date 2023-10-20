# -*- coding: utf-8 -*-
import os
import datetime

today = datetime.date.today()

def listFiles(dirPath):
    # 遍历指定文件夹下当天的sql文件
    fileList = []

    for root, dirs, files in os.walk(dirPath):

        for fileObj in files:
            filePath = os.path.join(root, fileObj)
            if os.path.splitext(fileObj)[1] == ".sql":
                # 获取文件的最后修改时间
                modification_time = os.path.getmtime(filePath)
                modification_date = datetime.date.fromtimestamp(modification_time)
                if modification_date == today:
                    fileList.append(filePath)

    return fileList
    retu

def replace_str(fileDir):
    replaceList = [["joinsaas_extjs_bff", "p00-b010"], ["joinsaas_tenant", "p00-v001"],
                   ["joinsaas_account", "p00-v002"], ["joinsaas_wechat", "p00-v003"],
                   ["joindbv_api", "p99-a000"], ["joinerp_coderule", "t01-v003"],
                   ["joinerp_datadict", "t01-v004"], ["joinerp_authoriz", "t01-v005"],
                   ["joinerp_approval", "t01-v007"], ["joinerp_finance", "t01-v008"],
                   ["joinerp_print", "t01-v009"], ["joinerp_setting", "t01-v010"],
                   ["joinerp_notification", "t01-v011"], ["joinfsc_product", "t02-v001"],
                   ["joinfsc_customer", "t02-v002"], ["joinfsc_supplier", "t02-v003"],
                   ["joinfsc_enquery", "t02-v004"], ["joinfsc_quote", "t02-v005"],
                   ["joinfsc_sales", "t02-v007"], ["joinfsc_customerstrategy", "t02-v008"],
                   ["joinfsc_purchase", "t02-v009"], ["joinfsc_distribute", "t02-v011"],
                   ["joinfsc_breakage", "t02-v013"], ["joinfsc_passbox", "t02-v014"],
                   ["joinfsc_reprocess", "t02-v015"], ["joinwms_warehouse", "t03-v001"],
                   ["joinwms_pickpack", "t03-v002"], ["joinwms_resource", "t05-v001"],
                   ["joinwms_shipment", "t05-v002"], ["joinwms_receiving", "t05-v003"],
                   ["joinwms_sorttask", "t05-v004"], ["joinwms_warehousingstrategy", "t05-v005"],
                   ["joinwms_inventorysum", "t05-v007"], ["joinwms_batchdetail", "t05-v008"],
                   ["joinwms_inventoryrecord", "t05-v009"], ["joinmcl_cookbook", "t04-v001"],
                   ["joinmcl_dish", "t04-v002"], ["joinmcl_wklymenu", "t04-v003"],
                   ["joinmcl_store", "t04-v004"], ["joinmcl_attendanceplan", "t04-v005"],
                   ["joinmcl_supplierinfo", "t04-v035"], ["joinerp_oss", "t01-v006"]]

    fileList = listFiles(fileDir)
    # 循环遍历列表内容
    for file_name in fileList:
        f = open(file_name, 'r+', encoding='ISO-8859-1')
        # readlines() 一次性读取所有行文件,可以遍历结果对每一行数据进行处理
        all_the_lines = f.readlines()
        # seek()方法，操作文件游标移动操作，0代表游标移动到文件开头
        f.seek(0)
        # truncate()方法，从光标所在位置进行截断【readlines() 一次性读取所有行文件，所以截取的就是全文】
        f.truncate()
        # 循环遍历文件内容的的每一行字段
        for line in all_the_lines:
            for replaceStr in replaceList:
                line = line.replace(replaceStr[0], replaceStr[1])
            f.write(line)
        # 关闭文件
        f.close()


if __name__ == '__main__':
    fileDir = os.getcwd()
    # fileDir = r'/Users/timpan/TP.CodeJX/JoinDbv.Views/join.ali/'

    replace_str(fileDir)
