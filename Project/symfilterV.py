import numpy as np
import time

# optimize
def symfilterV(X, H, k):
    H = np.array(H).astype(float)
    k_temp = k//2
    result = np.zeros_like(X, dtype=float)
    
    start = time.time()
    for row, data in enumerate(X):
        for num in range(0, k_temp):
            data = data.tolist()
            data.insert(0, X[row][num+1])
            data.append(X[row][len(X[row])-(num+2)])
            data = np.array(data, dtype=float)
        for col in range(len(data) - (k-1)):
            value = np.dot(data[col:col+k], H)
            result[row][col] = value

    end = time.time()
    print("Time in V = {:.5f}".format(end-start))
    
    return result