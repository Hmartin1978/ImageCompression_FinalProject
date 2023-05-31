import numpy as np

# def upsampleHorizontal(img1, img2):
#     # if(len(X) == 1): return X

#     rows, cols = img1.shape
#     new_cols = 2 * cols

#     result = np.zeros((rows, new_cols))
#     result[:, ::2] = img1
#     result[:, ::2] = img2

#     print(result.shape)
#     return 

def upsampleHorizontalLP(img):

    rows, cols = img.shape
    new_cols = 2 * cols

    result = np.zeros((rows, new_cols))
    result[:, ::2] = img

    return result

def upsampleHorizontalHP(img):

    rows, cols = img.shape
    new_cols = 2 * cols

    result = np.zeros((rows, new_cols))
    result[:, 1::2] = img

    return result