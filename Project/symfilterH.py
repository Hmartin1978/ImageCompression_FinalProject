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
        #     # ȡ��ת�ú��ÿһ�У�����Ԫ�ز�ֱ�Ӽ���
        #     for num in range(0, k_temp): # ȡX��ӦԪ��
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
            # ��ֱ�����һ������Ϊnp��֯����������������֯����Ԫ�ؼ�����������Ҫ��ת�ã��൱��������ת��Ϊ������������������ʽ���˲������
            # ȡ��ת�ú��ÿһ�У�����Ԫ�ز�ֱ�Ӽ���
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
