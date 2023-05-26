<<<<<<< HEAD
import numpy as np

x = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7]]
x = np.array(x)
x = x.transpose()
print(x)
x = x.transpose()
x = x.tolist()
print(x)
=======
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

d= defaultdict(list)
# d["a"].append([np.arange(-7,-4).flatten()]+[np.arange(4,7)])
# d["HL"].append([1,2,3])
# d["HL"].append([2,3,4,5])
# print(d["HL"][1])

# x = np.array([[-1,0,1],
#               [0,0,0],
#               [1,1,1]])

# print(np.sum(np.where(x[0:2,0:3], 1, 0)))

# x = (64, 64)

# 对于lowest来说，先prediction(flatten&latter-first)，然后有两个sequence：1.size&0 2.bianry bitstream(可以取巧转换为字符串,/8)
# 然后最其他frequency的subband使用EZW，同样得到各自的两个sequence：1.size&0&ZTR 2.bitstream，分别拼接在lowest的后面;一次性拿一个方向，不学EZW论文中的那个方向
# 只有第一个sequence需要用Huffman编码，第二个sequence直接传
# size可以直接编码为bitstream-amplitude还是当前值的大小？ ZTR又该编码为什么呢

def size_idx(val:int, size:str):
    power = ord(size) - ord("a") + 1
    init_val = -1 * np.power(2, power) + 1 if val < 0 else np.power(2, power) - 1
    idx = val - init_val if val < 0 else np.power(2, power) - (init_val - val) - 1
    return idx


print(bin(size_idx(-9,"d")))
>>>>>>> 81915ef (Encode is done, Next is Decode)
