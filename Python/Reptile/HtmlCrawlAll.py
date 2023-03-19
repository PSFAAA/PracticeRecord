import threading
from queue import Queue
import requests
from bs4 import BeautifulSoup
import os
import multiprocessing
import difflib


def fun(q, lst):
    HEADER = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"'
    }
    for page in lst:
        spider_url = 'https://www.shiyi.org.cn{}'.format(page)
        response = requests.get(spider_url, headers=HEADER).content.decode('gbk')
        soup = BeautifulSoup(response, 'lxml')
        if len(soup.find_all("span", {"class": "s2"})) > 0:  # 判断内容是否存在
            for span in soup.find_all("span", {"class": "s2"}):
                for a in span.find_all("a"):
                    q.append([a.attrs['href'], a.text])


# 获取书本目录
def getList(list_url, max_page):
    htmls = []
    for idx in range(1, max_page + 1):
        htmls.append(f"{list_url}{idx}.html")
    return htmls


def main():
    list_no = int(input('小说类型《玄幻》[1],《修真》[2],《都市》[3],《穿越》[4],《网游》[5],《科幻》[6],《其他》[7]' + '\n' + '请填写类型编号：'))
    if list_no == 1:
        list_url = r"/xuanhuanxiaoshuo/1_"
        max_page = 996
    elif list_no == 2:
        list_url = r"/xiuzhenxiaoshuo/2_"
        max_page = 226
    elif list_no == 3:
        list_url = r"/dushixiaoshuo/3_"
        max_page = 1244
    elif list_no == 4:
        list_url = r"/chuanyuexiaoshuo/4_"
        max_page = 158
    elif list_no == 5:
        list_url = r"/wangyouxiaoshuo/5_"
        max_page = 130
    elif list_no == 6:
        list_url = r"/kehuanxiaoshuo/6_"
        max_page = 1003
    else:
        list_url = r"/qitaxiaoshuo/7_"
        max_page = 878
    list_urls = getList(list_url, max_page)

    thread_input_list = dict()
    # 根据章节数选择合适的线程数量
    if len(list_urls) > 1000:
        thread_numbers = 200
    elif len(list_urls) > 500:
        thread_numbers = 100
    elif len(list_urls) > 200:
        thread_numbers = 50
    elif len(list_urls) > 50:
        thread_numbers = 4
    else:
        thread_numbers = 2
    partition_point = int(len(list_urls) / thread_numbers)
    for thread_number in range(0, thread_numbers):
        thread_input_list[thread_number] = list_urls[
                                           (thread_number * partition_point):(thread_number + 1) * partition_point]

    thread_position_list = dict()
    processes = dict()
    queues = dict()

    print("书本编号采集中...")

    lst = []
    with multiprocessing.Manager() as m:
        for thread in range(0, thread_numbers):
            queues[thread] = m.list()
            processes[thread] = multiprocessing.Process(target=fun,
                                                        args=(queues[thread], thread_input_list[thread]))
            processes[thread].start()

        for thread in range(0, thread_numbers):
            processes[thread].join()
            thread_position_list[thread] = queues[thread]

        for key, value in thread_position_list.items():
            lst.extend(value)
    # list排序
    # lst.sort(key=lambda x: x[0], reverse=False)
    # 嵌套list去重
    new_lst = []
    for item in lst:
        if item not in new_lst:
            new_lst.append(item)

    book_name = str(input('书本编号采集完毕!!!' + '\n' + '请输入关键词：'))
    # xz_list = []
    print('查询结果如下:')
    for xb in new_lst:
        if book_name in xb[1]:
            print(xb[0].replace('/', ''), xb[1])
            # xz_list.append(xb)
    # print(xz_list)


if __name__ == '__main__':
    main()
