import threading
from queue import Queue
import requests
from bs4 import BeautifulSoup
import os
import multiprocessing


# 采集数据
def ThreadCrawlPro(q, lst, is_download):
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
        if is_download == 1:
            if len(soup.find_all("h1")) > 0 and len(soup.find_all("div", {"id": "content"})) > 0:  # 判断内容是否存在
                eachPartName = soup.find_all("h1")[0].text  # 章节名
                eachContent = soup.find_all("div", {"id": "content"})[0].text  # 内容
                q.append([page[12:21], eachPartName, eachContent])
                print(eachPartName)
        else:
            if len(soup.find_all("span", {"class": "s2"})) > 0:  # 判断内容是否存在
                for span in soup.find_all("span", {"class": "s2"}):
                    for a in span.find_all("a"):
                        q.append([a.attrs['href'], a.text])


# 生成文件
def toFile(result, name):
    # 当前文件路径
    path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(path + '/book_txt'):
        os.makedirs(path + '/book_txt')
    # path = r'D:/book_txt/'
    with open(path + '/book_txt/' + name + '.txt', 'a', encoding='utf-8') as f:
        for i in result:
            f.write('\n\n' + i[1] + '\n\n')
            f.write(i[2])
    print("《", name, "》下载完毕！！！")


# 获取书本目录
def getBookList(list_url):
    list_urls = []
    r = requests.get("https://www.shiyi.org.cn" + list_url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, "html.parser")
    for div in soup.find_all("div", {"id": "list"}):
        for a in div.find_all("a"):
            list_urls.append(a.attrs['href'])
    del list_urls[0:9]
    return list_urls


# 获取书本名称
def fileName(list_url):
    file_name = ''
    r = requests.get("https://www.shiyi.org.cn" + list_url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, "html.parser")
    for div in soup.find_all("div", {"id": "info"}):
        file_name = div.find_all("h1")[0].text
    return file_name


# 设定线程数
def setThreadNum(list_urls):
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
    return thread_numbers


# 设定线程任务
def setThreadInputList(list_urls, thread_numbers):
    thread_input_list = dict()
    partition_point = int(len(list_urls) / thread_numbers)
    for thread_number in range(0, thread_numbers):
        thread_input_list[thread_number] = list_urls[
                                           (thread_number * partition_point):(thread_number + 1) * partition_point]
    return thread_input_list


# 执行多线程
def callThreadTasks(thread_numbers, thread_input_list, is_download):
    thread_position_list = dict()
    processes = dict()
    queues = dict()
    with multiprocessing.Manager() as m:
        for thread in range(0, thread_numbers):
            queues[thread] = m.list()
            processes[thread] = multiprocessing.Process(target=ThreadCrawlPro,
                                                        args=(queues[thread], thread_input_list[thread], is_download))
            processes[thread].start()

        for thread in range(0, thread_numbers):
            processes[thread].join()
            thread_position_list[thread] = queues[thread]

        lst = []
        for key, value in thread_position_list.items():
            lst.extend(value)
    return lst


# 下载书本
def downloadBook():
    print("--------------------------------------")
    list_url = "/" + input('请输入书本编号：') + "/"
    file_name = fileName(list_url)
    list_urls = getBookList(list_url)
    thread_numbers = setThreadNum(list_urls)
    thread_input_list = setThreadInputList(list_urls, thread_numbers)
    print("*******采集线程数:", thread_numbers, "已开启*******")
    print("已采集章节:")
    lst = callThreadTasks(thread_numbers, thread_input_list, 1)
    lst.sort(key=lambda x: x[0], reverse=False)
    toFile(lst, file_name)


# 获取书本目录
def getList(list_url, max_page):
    htmls = []
    for idx in range(1, max_page + 1):
        htmls.append(f"{list_url}{idx}.html")
    return htmls


# 加载书本编码
def downloadBookCode():
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
    thread_numbers = setThreadNum(list_urls)
    thread_input_list = setThreadInputList(list_urls, thread_numbers)
    print("书本编号采集中...")
    lst = callThreadTasks(thread_numbers, thread_input_list, 0)
    # 嵌套list去重
    new_lst = []
    for item in lst:
        if item not in new_lst:
            new_lst.append(item)

    book_name = str(input('书本编号采集完毕!!!' + '\n' + '请输入关键词：'))
    print('查询结果如下:')
    for xb in new_lst:
        if book_name in xb[1]:
            print(xb[0].replace('/', ''), xb[1])


def main():
    downloadBookCode()
    while True:
        downloadBook()


if __name__ == '__main__':
    main()
