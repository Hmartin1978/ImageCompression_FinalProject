#coding=gbk
import matplotlib.pyplot as plt
import numpy as np
from symfilterV import symfilterV
from symfilterH import symfilterH
from DownSamplingHorizontal import DownSamplingHorizontal
from DownSamplingVertical import DownSamplingVertical
from upsamleVertical import upsampleVertical
from upsamleHorizontal import upsampleHorizontal
from PSNR import PSNR

## filter
H0 = [-1/8, 1/4, 3/4, 1/4, -1/8]
H1 = [-1/2, 1, -1/2]
G0 = [1/2, 1, 1/2]
G1 = [-1/8, -1/4, 3/4, -1/4, -1/8]

# # 示例，检测能否完美重建
# X = np.arange(1, 513, dtype=np.float64)
# X = X.reshape(1, -1)
# X = np.arange(1,7, dtype=np.float64)
# X = X.reshape(1, -1)

def main(k):
    # load data
    lena = np.fromfile('image1.512', dtype=np.uint8)
    lena = lena.reshape(512, 512)

    X = np.empty((0, 512), dtype=float)
    for i, data in enumerate(lena):
        X = np.append(X, [data], 0)

    X0 = X
    A_list = []

    # DWT
    for i in range(k):
        U0 = symfilterV(X0, H0, 5)
        U1 = symfilterV(X0, H1, 3)
        Z, V0, V1 = DownSamplingHorizontal(U0, U1)

        B1 = symfilterH(V0, H0, 5)
        B2 = symfilterH(V0, H1, 3)
        B3 = symfilterH(V1, H0, 5)
        B4 = symfilterH(V1, H1, 3)
        Z1, A1, A2 = DownSamplingVertical(B1, B2) # LL, LH
        Z2, A3, A4 = DownSamplingVertical(B3, B4) # HL, HH

        X0 = A1
        if(i != k-1):
            # 保存其他方向的信息
            A_list.insert(0, A4)
            A_list.insert(0, A3)
            A_list.insert(0, A2) 

        
        # L = np.concatenate((A1, A2), axis=0)
        # H = np.concatenate((A3, A4), axis=0)
        # F = np.concatenate((L, H), axis=1)
        
    # IDWT
    for i in range(k):
        print("i = {}".format(i))

        D1 = upsampleVertical(A1) # LL
        D2 = upsampleVertical(A2) # LH
        D3 = upsampleVertical(A3) # HL
        D4 = upsampleVertical(A4) # HH

        C1 = symfilterH(D1, G0, 3)
        C2 = symfilterH(D2, G1, 5)
        C3 = symfilterH(D3, G0, 3)
        C4 = symfilterH(D4, G1, 5)

        W0 = upsampleHorizontal(C1 + C2)
        W1 = upsampleHorizontal(C3 + C4)


        Y0 = symfilterV(W0, G0, 3)
        Y1 = symfilterV(W1, G1, 5)

        Y = Y0 + Y1
        A1 = Y
        if(i != k-1):
            j = 3 * i
            A2 = A_list[j]
            A3 = A_list[j+1]
            A4 = A_list[j+2]

    print(PSNR(X, Y))

    show = np.concatenate((X,Y), axis=1)
    plt.imshow(show, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == "__main__":
    main(1)