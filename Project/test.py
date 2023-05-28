#coding=gbk
import numpy as np
from collections import defaultdict

# x = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7]]
# x = np.array(x)
# x = x.transpose()
# print(x)
# x = x.transpose()
# x = x.tolist()
# print(x)

# d= defaultdict(list)
# d["a"].append([np.arange(-7,-4).flatten()]+[np.arange(4,7)])
# d["HL"].append([1,2,3])
# # d["HL"].append([2,3,4,5])
# print(d.keys())
# for i in d.keys():
#     print(d[i])

# x = np.array([[-1,0,1],
#               [0,0,0],
#               [1,1,1]])

# print(np.sum(np.where(x[0:2,0:3], 1, 0)))

# x = (64, 64)

# 只有第一个sequence需要用Huffman编码，第二个sequence直接传
# size可以直接编码为bitstream-amplitude还是当前值的大小？ ZTR又该编码为什么呢

# print(bin(size_idx(-9,"d")))

# from collections import Counter

# # 示例字符串
# text = "abracadabra"

# # 使用Counter统计频率
# frequency = Counter(text)
# print(type(frequency))


# # # 打印结果
# # for char, count in frequency.items():
# #     print(char, ":", count)
# print(type(frequency.items()))

# # frequency = sorted(frequency.items(), key = lambda d : d[0])
# # print(frequency)

def size_idx(val:int, size:str):
    power = ord(size) - ord("a") + 1
    len = np.power(2, power)
    init_val = -1 * np.power(2, power) + 1 if val < 0 else np.power(2, power) - 1
    idx = val - init_val if val < 0 else np.power(2, power) - (init_val - val) - 1
    temp = bin(idx)[2:].zfill(power)


    print(temp)
    

# size_idx(-2, "b")

a = "abcd"
print(int("001101", 2))

