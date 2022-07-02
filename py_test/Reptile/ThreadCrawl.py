import os
import threading
from queue import Queue
import requests
from bs4 import BeautifulSoup

CRAWL_EXIT = False


class ThreadCrawl(threading.Thread):
    def __init__(self, thread_name, page_queue, data_queue, name_queue):
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = thread_name
        self.page_queue = page_queue
        self.data_queue = data_queue
        self.name_queue = name_queue

    def run(self):
        print(self.threadName + ' 启动************')
        while not CRAWL_EXIT:
            page = self.page_queue.get(block=False)  # 从里面获取值
            HEADER = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'Keep-Alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"'
            }
            if page < 10:
                spider_url = 'https://www.kanunu8.com/book3/6633/11600{}.html'.format(page)
            elif page == 35:
                continue
            else:
                spider_url = 'https://www.kanunu8.com/book3/6633/1160{}.html'.format(page)
            print(spider_url)
            response = requests.get(spider_url, headers=HEADER).content.decode('gbk')
            soup = BeautifulSoup(response, 'lxml')
            if self.name_queue.empty():
                self.name_queue.put(soup.find_all("table")[1].text[10:16])
            eachPartName = soup.find_all("table")[3].text  # 章节名
            eachContent = soup.find_all("table")[4].text  # 内容
            self.data_queue.put([eachPartName, eachContent])


def toFile(list, name):
    print(1)
    path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(path + '/{}'.format(name)):
        os.makedirs(path + '/{}'.format(name))
    for i in list:
        with open(path + '/{}/{}'.format(name, i[0]), 'w',
                  encoding='UTF-8') as f:
            f.write(i[1])


def main():
    # 声明一个队列，使用循环在里面存入100个页码
    page_queue = Queue(maxsize=0)
    for j in range(7, 40):
        page_queue.put(j)
    # 储存结果
    data_queue = Queue(maxsize=0)
    name_queue = Queue(1)
    craw_list = ['采集线程1号', '采集线程2号', '采集线程3号', '采集线程4号']
    for thread_name in craw_list:
        c_thread = ThreadCrawl(thread_name, page_queue, data_queue, name_queue)
        c_thread.start()
    while not page_queue.empty():
        pass
    global CRAWL_EXIT
    CRAWL_EXIT = True
    name = name_queue.get()
    result = []
    for i in range(7, 39):
        result.append(data_queue.get())
    print(result)
    print(name)
    toFile(result, name)


if __name__ == '__main__':
    main()
