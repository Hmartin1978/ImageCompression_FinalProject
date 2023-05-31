#coding=gbk
import numpy as np
import time

def symfilterH(X, H, k):
    # H = np.array(H).astype(float)
    k_temp = k // 2 
    X_copy = X
    X_copy = np.transpose(X_copy)
    result = np.zeros_like(X_copy, dtype=np.float32)

    if(len(X) == 1): 
        # start = time.time()
        # for row, data in enumerate(X_copy):
        #     # 取出转置后的每一行，插入元素并直接计算
        #     for num in range(0, k_temp): # 取X对应元素
        #         data = data.tolist()
        #         data.insert(0, X[0][row])
        #         data.append(X[0][row])
        #         data = np.array(data, dtype=float)
        #     for col in range(len(data) - (k-1)):
        #         value = np.dot(data[col:col+k], H)
        #         result[row][0] = value
        # end = time.time()
        # print("Time in H = {:.5f}s".format(end-start))
        # result = np.transpose(result)
        # return result
        return X

    else: 
        # start = time.time()
        for row, data in enumerate(X_copy):
            # 垂直情况不一样，因为np组织矩阵都是以行向量组织，补元素及后续计算需要做转置；相当于列向量转置为行向量再与行向量形式的滤波器相乘
            # 取出转置后的每一行，插入元素并直接计算
            data = data.tolist()
            for num in range(0, k_temp):
                data.insert(0, X[num+1][row])
                data.append(X[len(X)-(num+2)][row])
            data = np.array(data, dtype=float)
            for col in range(len(data) - (k-1)):
                value = np.dot(data[col:col+k], H)
                result[row][col] = value
        # end = time.time()
        # print("Time in H = {:.5f}s".format(end-start))
        result = np.transpose(result)

        return result
