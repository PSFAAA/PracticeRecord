# import random
import time
import re
import json
import requests
from bs4 import BeautifulSoup


# 0818页面读取
class WebTextsRead:
    def __init__(self, page_nums):
        self.page_nums = int(page_nums)

    def web_text(self):
        max_pg_num = self.page_nums
        cases = []
        for page in range(0, max_pg_num):
            resp = requests.get(
                url=f'http://www.0818tuan.com/list-1-{page}.html',
                # 通过get函数的headers参数设置User-Agent的值，具体的值可以在浏览器的开发者工具查看到。
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
            )

            soup = BeautifulSoup(resp.text, 'lxml')

            for k in soup.find_all('a', {'target': '_blank', 'class': 'list-group-item'}, limit=40):
                case = {}
                pattern = re.compile(r'<span class="badge badge-success red">([^&]*?)</span>')
                k_time = pattern.findall(str(k))
                case['time'] = k_time[0]
                case['title'] = k['title']
                case['href'] = 'http://www.0818tuan.com' + k['href']
                cases.append(case)
                # print(k_time[0], k['title'], 'http://www.0818tuan.com' + k['href'])
            # time.sleep(random.random() * 3 + 1)
            time.sleep(1)
        return cases

    def get_json(self):
        print(json.dumps(self.web_text(), ensure_ascii=False))


def main():
    r"""
    """
    wtr = WebTextsRead(input('读取页数：'))
    wtr.get_json()


if __name__ == '__main__':
    main()

