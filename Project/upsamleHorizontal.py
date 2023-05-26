import numpy as np

<<<<<<< HEAD
def upsampleHorizontal(X):
    # if(len(X) == 1): return X

    rows, cols = X.shape
    new_cols = 2 * cols 

    result = np.zeros((rows, new_cols))
    result[:, ::2] = X
=======
def upsampleHorizontal(img1, img2):
    # if(len(X) == 1): return X

    rows, cols = img1.shape
    new_cols = 2 * cols 

    result = np.zeros((rows, new_cols))
    result[:, ::2] = img1
    result[:, 1::2] = img2
>>>>>>> 81915ef (Encode is done, Next is Decode)

    print(result.shape)
    return result