import urllib.request as ur
import os
import easygui as e
import time
import requests
from lxml import etree
import re
import json
from bs4 import BeautifulSoup


def url_open(url):
    time.sleep(0.1)
    req = ur.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/80.0.3987.116 Safari/537.36")

    response = ur.urlopen(req)
    html = response.read()

    return html


# def find_next(html):
#     # a = html.find("url_next:", 0, -1)
#     # b = html.find(",", a, a + 128)
#     # return html[a + 10: b - 1]
#
#     return pattern


def find_title(html):
    a = html.find("mlfy_main_text")
    b = html.find("</h1>", a, a + 255)
    title = html[a + 24: b]
    return title


def find_content(html):
    content = []
    start = html.find("content", 0, -1)
    end = html.find("投推荐票", start, -1)

    a = html.find("<p>", start, end)
    while a < end:
        b = html.find("</p>", a, -1)
        if b < end:
            content.append(html[a + 3: b])
        else:
            break
        a = html.find("<p>", b + 3, -1)
    return content


def save_file(file_name, title, content_list):
    f = open(file_name, "a+", encoding="UTF-8")
    f.write(title + "\n\n")
    for content in content_list:
        f.write("    " + content + "\n\n")
    f.close()


def main():
    # html = url_open("https://www.shiyi.org.cn/228_228064/195021146.html").decode("gbk")
    url_next = "/228_228064/195021116.html"
    while url_next == "/228_228064/195021116.html":
        html = url_open("https://www.shiyi.org.cn" + url_next).decode("gbk")
        # 找到标题
        # my_title = find_title(html)
        # print(my_title)
        # 找到内容
        # my_contents = find_content(html)
        # print(my_contents)
        # print(html)
        # 保存成txt
        # save_file("demo.txt", my_title, my_contents)
        # print("保存完毕")
        # 找到下个网址
        soup = BeautifulSoup(html.text, 'lxml')

        for k in soup.find_all('a', limit=40):
            case = {}
            pattern = re.compile(r'<a href = "([^&]*?)> 下一章 </a>')
            k_time = pattern.findall(str(k))

            print(k['href'])

        url_next = find_next(html)
        print(url_next)


if __name__ == "__main__":
    main()
