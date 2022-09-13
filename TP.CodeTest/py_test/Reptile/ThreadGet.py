from concurrent.futures import ThreadPoolExecutor
import time
import random


def load_data(char):
    num = random.randint(1, 15)
    time.sleep(num)
    return char + str(num)


char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

with ThreadPoolExecutor(10) as executor:
    for n, result in zip(char_list, executor.map(load_data, char_list)):
        print("%r page status_code %s" % (n, result))
