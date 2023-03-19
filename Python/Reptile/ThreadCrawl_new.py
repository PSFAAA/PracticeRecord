import threading
from queue import Queue
import requests
from bs4 import BeautifulSoup
import os

CRAWL_EXIT = False


class ThreadCrawl(threading.Thread):
    def __init__(self, page_queue, data_queue):
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.page_queue = page_queue
        self.data_queue = data_queue

    def run(self):
        while not CRAWL_EXIT:
            while not self.page_queue.empty():
                page = self.page_queue.get(block=False)  # 从里面获取值
                HEADER = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'Keep-Alive',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
                    'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"'
                }
                spider_url = 'https://www.shiyi.org.cn{}'.format(page)
                response = requests.get(spider_url, headers=HEADER).content.decode('gbk')
                soup = BeautifulSoup(response, 'lxml')
                if len(soup.find_all("h1")) > 0 and len(soup.find_all("div", {"id": "content"})) > 0:  # 判断内容是否存在
                    eachPartName = soup.find_all("h1")[0].text  # 章节名
                    eachContent = soup.find_all("div", {"id": "content"})[0].text  # 内容
                    self.data_queue.put([page.split("/")[2], eachPartName, eachContent])
                    print(eachPartName)


def toFile(result, name):
    # 当前路径
    path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(path + '/book_txt'):
        os.makedirs(path + '/book_txt')
    # path = r'D:/xiaoshuo/'
    with open(path + '/book_txt/' + name + '.txt', 'a', encoding='utf-8') as f:
        for i in result:
            f.write('\n\n' + i[1] + '\n\n')
            f.write(i[2])
    print("小说下载完毕！！！")


def getList(list_url):
    list_urls = []
    r = requests.get("https://www.shiyi.org.cn" + list_url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, "html.parser")
    for div in soup.find_all("div", {"id": "list"}):
        for a in div.find_all("a"):
            # print(a.attrs['href'])
            list_urls.append(a.attrs['href'])
    del list_urls[0:9]
    # print(content)
    return list_urls


def fileName(list_url):
    r = requests.get("https://www.shiyi.org.cn" + list_url)
    r.encoding = 'gbk'
    soup = BeautifulSoup(r.text, "html.parser")
    for div in soup.find_all("div", {"id": "info"}):
        file_name = div.find_all("h1")[0].text
    return file_name


def main():
    global CRAWL_EXIT
    list_url = "/" + input('书本编号：') + "/"
    # list_url = "/228_228064/"
    # file_name = '玄幻，我能无限顿悟'
    file_name = fileName(list_url)
    list_urls = getList(list_url)
    # list_urls = ['/228_228064/195021116.html',
    #              '/228_228064/195021119.html',
    #              '/228_228064/195021122.html']
    # 声明一个队列，使用循环在里面存入100个页码
    page_queue = Queue(maxsize=0)
    for j in list_urls:
        page_queue.put(j)
    # 储存结果
    data_queue = Queue(maxsize=0)
    print("*******采集线程1~200号 已开启*******")
    print("已采集章节:")
    for thread_no in range(0, 200):
        c_thread = ThreadCrawl(page_queue, data_queue)
        c_thread.start()
    CRAWL_EXIT = True
    result = []
    # for i in range(0, len(list_urls)):
    for i in range(0, 200):
        result.append(data_queue.get())
    result.sort(key=lambda x: x[0], reverse=False)
    toFile(result, file_name)
    print(result)


if __name__ == '__main__':
    main()
