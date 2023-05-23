#coding=gbk
import numpy as np
import time


# def symfilterV(X, H, k):
#     H = np.array(H).astype(float)
#     result = np.zeros_like(X, dtype=np.float64)

#     k_temp = k // 2 # 针对k=3需要单独操作
#     XStart_temp = [0 for i in range(k_temp)] if k_temp > 1 else [0] * k_temp# 列表推导初始化列表
#     XEnd_temp = [0] * (k_temp) if  k_temp > 1 else [0] * k_temp# *运算符初始化列表

#     start = time.time()
#     for idx, _ in enumerate(X):
#         # 对称补元素
#         for i in range(0, k_temp):
#             XStart_temp[i] = X[idx][i+1]
#             XEnd_temp[i] = X[idx][len(X[idx])-(i+2)]
#         for i in range(k_temp):
#             list(X[idx]).insert(0, XStart_temp[i])
#             list(X[idx]).append(XEnd_temp[i])
            
#     # 滤波器计算
#     X = np.array(X)
#     X = X.astype(float)
#     for row, _ in enumerate(X):
#         for col in range(len(X[row]) - (k-1)):
#             value = np.dot(X[row][col:col+k], H)
#             result[row][col] = value
#     end = time.time()
#     print("Time in V = {:.5f}s\n".format(end-start))

#     return result

# optimize
def symfilterV(X, H, k):
    H = np.array(H).astype(np.float64)
    k_temp = k//2
    result = np.zeros_like(X, dtype=np.float64)
    
    start = time.time()
    for row, data in enumerate(X):
        for num in range(0, k_temp):
            data = data.tolist()
            data.insert(0, X[row][num+1])
            data.append(X[row][len(X[row])-(num+2)])
            data = np.array(data, dtype=np.float64)
        for col in range(len(data) - (k-1)):
            value = np.dot(data[col:col+k], H)
            result[row][col] = value

    end = time.time()
    print("Time in V = {:.5f}".format(end-start))
    
    return result

# x = [[1,2,3,4,5]]
# H = [1,0,1]
# symfilterV(x, H, 3)