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

# ����lowest��˵����prediction(flatten&latter-first)��Ȼ��������sequence��1.size&0 2.bianry bitstream(����ȡ��ת��Ϊ�ַ���,/8)
# Ȼ��������frequency��subbandʹ��EZW��ͬ���õ����Ե�����sequence��1.size&0&ZTR 2.bitstream���ֱ�ƴ����lowest�ĺ���;һ������һ�����򣬲�ѧEZW�����е��Ǹ�����
# ֻ�е�һ��sequence��Ҫ��Huffman���룬�ڶ���sequenceֱ�Ӵ�
# size����ֱ�ӱ���Ϊbitstream-amplitude���ǵ�ǰֵ�Ĵ�С�� ZTR�ָñ���Ϊʲô��

def size_idx(val:int, size:str):
    power = ord(size) - ord("a") + 1
    init_val = -1 * np.power(2, power) + 1 if val < 0 else np.power(2, power) - 1
    idx = val - init_val if val < 0 else np.power(2, power) - (init_val - val) - 1
    return idx


print(bin(size_idx(-9,"d")))
>>>>>>> 81915ef (Encode is done, Next is Decode)
