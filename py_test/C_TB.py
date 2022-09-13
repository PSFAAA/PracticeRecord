#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import time
import json
import re

LOG_LINE_NUM = 0


class MyGui:
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.init_data_text = Text(self.init_window_name, width=67, height=30)  # 原始数据录入框
        self.result_data_text = Text(self.init_window_name, width=70, height=49)  # 处理结果展示
        self.log_data_text = Text(self.init_window_name, width=66, height=10)  # 日志框
        self.init_table_name = Text(self.init_window_name, width=66, height=2)  # 中文表名录入框
        self.str_trans_to_md5_button = Button(self.init_window_name, text="超进化", bg="lightblue", width=10,
                                              command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.init_table_label = Label(self.init_window_name, text="中文表名")
        self.log_label = Label(self.init_window_name, text="日志")
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.init_data_label = Label(self.init_window_name, text="待处理数据")

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("建表偷懒工具_v0.01")  # 窗口名
        # self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        # self.init_window_name["bg"] = "pink"
        # #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887 self.init_window_name.attributes("-alpha",
        # 0.9)
        # #虚化，值越小虚化程度越高 标签
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label.grid(row=0, column=12)
        self.log_label.grid(row=11, column=0)
        self.init_table_label.grid(row=8, column=0)
        # 文本框
        self.init_data_text.grid(row=1, column=0, rowspan=6, columnspan=10)
        self.result_data_text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_text.grid(row=12, column=0, columnspan=10)
        self.init_table_name.grid(row=9, column=0, columnspan=10)
        # 按钮
        self.str_trans_to_md5_button.grid(row=4, column=11)

    # 功能函数
    def str_trans_to_md5(self):
        data_model = None
        # text = str(self.init_data_Text.get(1.0,END).strip().replace("\n","").encode('utf-8'))
        tb_name = str(self.init_table_name.get(1.0, END).strip().replace("\n", ""))
        text = "{" + str(self.init_data_text.get(1.0, END).strip().replace("\n", "").replace(" ", "")) + "]}"
        text = text.replace('tableName', "'tableName'")
        text = text.replace('alias', "'alias'")
        text = text.replace('name', "'name'")
        text = text.replace('fields', "'fields'")
        text = text.replace("'type'", "type")
        text = text.replace('type', "'type'")
        text = text.replace('display', "'display'")
        text = text.replace('reference', "'reference'")
        text = text.replace('inverse', "'inverse'")
        text = text.replace('dateFormat', "'dateFormat'")
        text = text.replace('picker', "'dateFormat'")
        text = text.replace("'", '"')
        text = text.replace('boolean', 'TINYINT(1) DEFAULT 0')
        text = text.replace('bool', 'TINYINT(1) DEFAULT 0')
        text = text.replace('string', 'VARCHAR(50) DEFAULT NULL')
        text = text.replace('number', 'DECIMAL(10,4) DEFAULT 0.0000')
        text = text.replace('date', 'DATETIME DEFAULT NULL')
        text = text.replace('int', 'INT(11) DEFAULT NULL')
        text = text.replace('model.', '')
        text = text.replace(',}', '}')
        text = text.replace(',]}', ']}')
        # 新增正则表达式去除多余备注
        # text = re.sub(r',[]]?}', '}', text)
        text = re.sub(r'//[\u4e00-\u9fa5_a-zA-Z0-9 \n，,]*', '', text)
        # print(text)
        self.result_data_text.delete(1.0, END)
        try:
            data_model = json.loads(text)
        except json.decoder.JSONDecodeError:
            self.result_data_text.insert(1.0, "进化失败,请查找输入框数据错误！！！")
            self.write_log_to_text("ERROR:json解析错误")
        # print(data_model)
        try:
            sc_code = "CREATE TABLE `%s` (\n" % data_model['alias']
        except KeyError:
            sc_code = "CREATE TABLE `%s` (\n" % data_model['tableName']
        # sc_code = "CREATE TABLE `%s` (" % data_model['alias']
        # sc_code = text
        self.result_data_text.insert(1.0, sc_code)
        self.result_data_text.insert(2.0, "`KID` INT(11) NOT NULL AUTO_INCREMENT COMMENT '主键',\n")
        self.result_data_text.insert(3.0, "`CID` INT(11) NOT NULL COMMENT '所有者(ID)',\n")
        nums = 3.0
        # print(nums)
        for tbls in data_model['fields']:
            if tbls["name"] == 'PID':
                nums += 1
                self.result_data_text.insert(nums, "`PID` INT(11) NOT NULL COMMENT '%s',\n" % tbls["display"])
            elif tbls["name"] != 'CID':
                nums += 1
                self.result_data_text.insert(nums,
                                             "`%s` %s COMMENT '%s',\n" % (tbls["name"], tbls["type"], tbls["display"]))
            # print(nums)
        self.result_data_text.insert(nums + 1, "`CRT_CODE` VARCHAR(50) NOT NULL COMMENT '创建人',\n")
        self.result_data_text.insert(nums + 2, "`CRT_TIME` DATETIME NOT NULL COMMENT '创建日期',\n")
        self.result_data_text.insert(nums + 3, "`MDF_CODE` VARCHAR(50) DEFAULT NULL COMMENT '修改人',\n")
        self.result_data_text.insert(nums + 4, "`MDF_TIME` DATETIME DEFAULT NULL COMMENT '修改日期',\n")
        self.result_data_text.insert(nums + 5, "`IS_DELETE` TINYINT(1) DEFAULT 0 COMMENT '是否删除? 0:否 1:是',\n")
        self.result_data_text.insert(nums + 6, "`VID` CHAR(36) NOT NULL COMMENT '版本主键',\n")
        self.result_data_text.insert(nums + 7, "PRIMARY KEY (`KID`)\n")
        self.result_data_text.insert(nums + 8, ") ENGINE=INNODB DEFAULT CHARSET=utf8 COMMENT='%s';" % tb_name)
        self.write_log_to_text("进化成功！！！")

    # 获取当前时间
    @staticmethod
    def get_current_time():
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_log_to_text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 7:
            self.log_data_text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_text.delete(1.0, 2.0)
            self.log_data_text.insert(END, logmsg_in)


def main():
    r"""
alias: 'model.b_supplierquote_detail',
    fields: [
        {
            name: 'PID', type: 'int', display: "主表ID",
            reference: {
                type: 'SupplierQuote.X',
                inverse: 'XDetail'
            }
        },
        { name: 'PRODUCT_CATEGORY_CODE', type: 'string', display: "产品类别CODE" },
        { name: 'PRODUCT_CATEGORY_NAME', type: 'string', display: "产品类别" },
        { name: 'PRODUCT_CODE', type: 'string', display: "产品编码" },
        { name: 'PRODUCT_NAME', type: 'string', display: "产品名称" },
        { name: 'BASE_UNIT', type: 'string', display: "基础单位" },
        { name: 'SPEC_DESCRIBE', type: 'string', display: "规格描述" },
        { name: 'SPEC_UNIT', type: 'string', display: "规格单位" },
        { name: 'CURRENT_QUOTE', type: 'number', display: "本期报价" },
        { name: 'GUIDANCE_PRICE', type: 'auto', display: "本期指导价" },
        { name: 'CURRENT_PRICE', type: 'auto', display: "本期定价" },
        { name: 'BASE_PRICE', type: 'number', display: "基本单位定价（￥）" },
        { name: 'MAX_SUPPLY_NUM', type: 'number', display: "最大供货量" },
        { name: 'BID_NUM', type: 'number', display: "中标" },
    """
    init_window = Tk()  # 实例化出一个父窗口
    zmj_portal = MyGui(init_window)
    # 设置根窗口默认属性
    zmj_portal.set_init_window()

    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    main()
