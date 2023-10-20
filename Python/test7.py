# 计算top10的单词
from collections import Counter


# import re
# text = 'remove an existing key one level down remove an existing key one level down'
# words = re.findall(r'\w+', text)
# print(Counter(words).most_common(10))
# # [('remove', 2),('an', 2),('existing', 2),('key', 2),('one', 2)('level', 2),('down', 2)]

def str_sim(str_0, str_1, topn):
    topn = int(topn)
    collect0 = Counter(dict(Counter(str_0).most_common(topn)))
    collect1 = Counter(dict(Counter(str_1).most_common(topn)))
    jiao = collect0 & collect1
    bing = collect0 | collect1
    sim = float(sum(jiao.values())) / float(sum(bing.values()))
    return (sim)


str_0 = '定位手机定位汽车定位GPS定位人定位位置查询'
str_1 = '导航定位手机定位汽车定位GPS定位人定位位置查询'

print(str_sim(str_0, str_1, 5))
