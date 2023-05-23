#coding=gbk
import numpy as np
import time

def symfilterH(X, H, k):
    H = np.array(H).astype(np.float64)
    k_temp = k // 2 
    X_copy = X
    X_copy = np.transpose(X_copy)
    result = np.zeros_like(X_copy, dtype=np.float64)

    if(len(X) == 1): 
        start = time.time()
        for row, data in enumerate(X_copy):
            # ȡ��ת�ú��ÿһ�У�����Ԫ�ز�ֱ�Ӽ���
            for num in range(0, k_temp): # ȡX��ӦԪ��
                data = data.tolist()
                data.insert(0, X[0][row])
                data.append(X[0][row])
                data = np.array(data, dtype=np.float64)
            for col in range(len(data) - (k-1)):
                value = np.dot(data[col:col+k], H)
                result[row][0] = value
        end = time.time()
        print("Time in H = {:.5f}s".format(end-start))
        result = np.transpose(result)

        return result

    else: 
        start = time.time()
        for row, data in enumerate(X_copy):
            # ȡ��ת�ú��ÿһ�У�����Ԫ�ز�ֱ�Ӽ���
            for num in range(0, k_temp): # ȡX��ӦԪ��
                data = data.tolist()
                data.insert(0, X[num+1][row])
                data.append(X[len(X)-(num+2)][row])
                data = np.array(data, dtype=np.float64)
            for col in range(len(data) - (k-1)):
                value = np.dot(data[col:col+k], H)
                result[row][col] = value
        end = time.time()
        print("Time in H = {:.5f}s".format(end-start))
        result = np.transpose(result)

        return result

    # # ���ȶ����к�
    # for idx in range(len(X[0])): # �� 
    #     # ��ֱ�����һ������Ϊnp��֯����������������֯����Ԫ�ؼ�����������Ҫ��ת�ã��൱��������ת��Ϊ������������������ʽ���˲������
    #     for i in range(0, k_temp): # ��
    #         XStart_temp[i] = X[i+1][idx]
    #         XEnd_temp[i] = X[len(X)-(i+2)][idx]
    #     X = np.array(X)
    #     X = X.transpose() # 256x512
    #     X = X.tolist()
    #     for i in range(k_temp):
    #         X[idx].insert(0, XStart_temp[i])
    #         X[idx].append(XEnd_temp[i])

    # # �˲�������(��������תΪ���������м��㣬��ת�û�ȥ)
    # start = time.time()
    # X = np.array(X)
    # for row, _ in enumerate(X):
    #     for col in range(len(X[row]) - (k-1)):
    #         value = np.dot(X[row][col:col+k], H)
    #         sum = np.sum(value)
    #         result[row][col] = sum
    # X = X.transpose()
    # result = result.transpose()
    # print(result)
    # end = time.time()
    # print("Time = {}s\n".format(end-start))

# x = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7],[4,5,6,7,8],[5,6,7,8,9]]
# H = [1,0,0,0,1]
# symfilterH(x,H,5)