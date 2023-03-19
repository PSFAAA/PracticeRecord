import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
import os


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


# 获取内容
def getText(page, name):
    # r = requests.get(url)
    # r.encoding = 'gbk'
    # selector = etree.HTML(r.text)
    # title = selector.xpath('//h1/text()')
    # text = selector.xpath('//*[@id="content"]/text()')
    # url_next = re.compile(r'<a href="([^"]*)"[^>]*>下一章</a>').findall(r.text)
    # print('已下载章节:', title[0])
    # with open(path + '我能无限顿悟.txt', 'a', encoding='utf-8') as f:
    #     f.write('\n\n' + title[0] + '\n\n')
    #     for i in text:
    #         f.write(i)
    # return url_next[0]

    HEADER = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"'
    }
    spider_url = 'https://www.shiyi.org.cn{}'.format(page)
    response = requests.get(spider_url, headers=HEADER).content.decode('gbk')
    soup = BeautifulSoup(response, 'lxml')
    eachPartName = soup.find_all("h1")[0].text  # 章节名
    eachContent = soup.find_all("div", {"id": "content"})[0].text  # 内容
    print('已下载章节:', eachPartName)
    path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(path + '/book_txt'):
        os.makedirs(path + '/book_txt')
    with open(path + '/book_txt/' + name + '.txt', 'a', encoding='utf-8') as f:
        f.write('\n\n' + eachPartName + '\n\n')
        f.write(eachContent)


def main():
    list_url = "/" + input('书本编号：') + "/"
    # list_url = "/228_228064/"
    # file_name = '玄幻，我能无限顿悟'
    file_name = fileName(list_url)
    list_urls = getList(list_url)
    for j in list_urls:
        getText(j, file_name)


if __name__ == '__main__':
    main()
