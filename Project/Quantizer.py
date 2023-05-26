import numpy as np

def Quantization(X, q):
    # if element > 0, use floor; else use round
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if X[i][j] / q > 0:
                X[i][j] = np.floor(X[i][j] / q)
            else:
                X[i][j] = np.round(X[i][j] / q)
    return X.astype(int)

def DeQuantization(X, q):
    X = np.round(X * q)
    return X