import numpy as np

def DownSamplingVertical(U0, U1):
    if(len(U0) == 1):
        return None, U0, U1
    
    V0 = U0[::2, :]
    V1 = U1[::2, :]
    result = np.vstack((V0, V1)).astype(np.float64)
    
    return result, V0, V1