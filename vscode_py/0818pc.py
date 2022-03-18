import random
import re
import time

import requests
from bs4 import BeautifulSoup

for page in range(0, 5):
    resp = requests.get(
        url=f'http://www.0818tuan.com/list-1-{page}.html',
        # 通过get函数的headers参数设置User-Agent的值，具体的值可以在浏览器的开发者工具查看到。
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        )

    soup = BeautifulSoup(resp.text, 'lxml')

    for k in soup.find_all('a', {'target': '_blank', 'class': 'list-group-item'}, limit=40):
        print(k['title'], ':', 'http://www.0818tuan.com'+k['href'])

    time.sleep(random.random() * 4 + 1)
