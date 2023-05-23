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

lena = np.fromfile('image1.512', dtype=np.uint8)
lena = lena.reshape(512, 512)

X = np.empty((0, 512), dtype=np.float64)
for i, data in enumerate(lena):
    X = np.append(X, [data], 0)


# 示例，检测能否完美重建
X = np.arange(1, 513, dtype=np.float64)
X = X.reshape(1, -1)



## filter
H0 = [-1/8, 1/4, 3/4, 1/4, -1/8]
H1 = [-1/2, 1, -1/2]
G0 = [1/2, 1, 1/2]
G1 = [-1/8, -1/4, 3/4, -1/4, -1/8]

X0 = X

for i in range(3):


    U0 = symfilterV(X0, H0, 5)
    U1 = symfilterV(X0, H1, 3)
    plt.subplot(221),plt.title('U0'), plt.imshow(U0, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])

    Z, V0, V1 = DownSamplingHorizontal(U0, U1)
    plt.subplot(222),plt.title('V0'), plt.imshow(V0, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])

    # 垂直滤波有问题，导致下方出现过多0
    B1 = symfilterH(V0, H0, 5)
    B2 = symfilterH(V0, H1, 3)
    B3 = symfilterH(V1, H0, 5)
    B4 = symfilterH(V1, H1, 3)
    plt.subplot(223),plt.title('B1'), plt.imshow(B1, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])

    Z1, A1, A2 = DownSamplingVertical(B1, B2)
    Z2, A3, A4 = DownSamplingVertical(B3, B4)
    plt.subplot(224),plt.title('A1'), plt.imshow(A1, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])

    X0 = A1
    # X0 = X0.astype(int)
    
    # L = np.concatenate((A1, A2), axis=0)
    # H = np.concatenate((A3, A4), axis=0)
    # F = np.concatenate((L, H), axis=1)
    
    # plt.subplot(2,2,2), plt.imshow(H, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    # plt.subplot(2,2,3), plt.imshow(A3, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    # plt.subplot(2,2,4), plt.imshow(A4, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    # plt.tight_layout()
    # plt.show()

# for i in range(1):
#     D1 = upsampleVertical(A1)
#     D2 = upsampleVertical(A2)
#     D3 = upsampleVertical(A3)
#     D4 = upsampleVertical(A4)

#     C1 = symfilterH(D1, G0, 3)
#     C2 = symfilterH(D2, G1, 5)
#     C3 = symfilterH(D3, G0, 3)
#     C4 = symfilterH(D4, G1, 5)

#     W0 = upsampleHorizontal(C1 + C2)
#     W1 = upsampleHorizontal(C3 + C4)

#     Y0 = symfilterV(W0, G0, 3)
#     Y1 = symfilterV(W1, G1, 5)

#     Y = Y0 + Y1
#     # Y /= 2

# plt.subplot(1,2,2), plt.imshow(Y, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])

# print(PSNR(X, Y))

plt.show()

