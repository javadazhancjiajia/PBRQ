from GrayCode import Gray
from PBRQ2 import PBQTree2, search_PBRQ2
from PBRQ import PBQTree, search_PBRQ
import time
from shve.SHVE import SHVE
from tool import get_test_data
import math


if __name__ == '__main__':
    key_len = 100
    t = 10 ** 4
    gray_bit = math.ceil(math.log2(t))

    print('read key_set and data_set')
    time1 = time.time()
    key_set, data_set = get_test_data('test_data/10x10/100', 'test_data/10x10/10x10_100_1.csv', 10000)
    time2 = time.time()
    print(
        f'finish\nsize of key_set:{key_set.__len__()}\nsize of data_set:{data_set.__len__()}\ncost time:{time2 - time1}')

    time1 = time.time()
    gray = Gray(gray_bit, gray_bit)
    r1 = time.time() - time1

    # 建树
    # time1 = time.time()
    # test1 = PBQTree(t, gray)
    # test1.create_tree()
    # test1.insert_data(key_set, data_set)
    # time2 = time.time()
    # print(f'PBQTree build tree:{time2-time1+r1}')
    # exit(0)

    key_shve = SHVE(key_len)
    gray_shve = SHVE(gray_bit * 2)
    # 建树
    time1 = time.time()
    test2 = PBQTree2(t, gray, gray_shve, key_shve)
    test2.create_tree(key_set, data_set)
    time2 = time.time()
    print(f'PBQTree2 build tree:{time2-time1+r1}')
    exit(1)

    # 测试
    area = [
        (7175, 7175)
    ]
    test_area = [area, 1]

    s = [1]
    m = ""
    for i in range(key_len, 0, -1):
        if i in s:
            m += "1"
        else:
            m += "*"
    test_area1 = [[gray_shve.trap_door("0000000***0000000***")], gray_shve.encrypt(2050), key_shve.trap_door(m)]

    # rec = []
    # time1 = time.time()
    # search_PBRQ(test1.root, test_area, rec)
    # time2 = time.time()
    # print(f'PBQTree search time:{time2-time1}\nsize of result:{rec.__len__()}条')

    rec2 = []
    time1 = time.time()
    search_PBRQ2(test2.root, test_area1, rec2, gray_shve)
    time2 = time.time()
    print(f'PBQTree2 search time:{time2 - time1}\nsize of result:{rec2.__len__()}条')