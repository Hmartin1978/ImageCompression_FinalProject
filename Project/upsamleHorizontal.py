import numpy as np

def upsampleHorizontal(X):
    # if(len(X) == 1): return X

    rows, cols = X.shape
    new_cols = 2 * cols 

    result = np.zeros((rows, new_cols))
    result[:, ::2] = X

    print(result.shape)
    return result