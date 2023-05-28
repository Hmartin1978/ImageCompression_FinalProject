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
import Quantizer
from collections import defaultdict
from Encoder import RLE
from Decoder import Decode
from HuffmanEncode import HuffmanEncode, HuffmanDecode


## filter
H0 = [-1/8, 1/4, 3/4, 1/4, -1/8]
H1 = [-1/2, 1, -1/2]
G0 = [1/2, 1, 1/2]
G1 = [-1/8, -1/4, 3/4, -1/4, -1/8]


def main(k):
    # load data
    lena = np.fromfile('image1.512', dtype=np.uint8)
    lena = lena.reshape(512, 512)

    X = np.empty((0, 512), dtype=float)
    for i, data in enumerate(lena):
        X = np.append(X, [data], 0)

    # # 示例，检测能否完美重建
    # X = np.arange(1, 513, dtype=np.float64)
    # X = X.reshape(1, -1)
    # X = np.arange(1,7, dtype=np.float64)
    # X = X.reshape(1, -1)

    X0 = X
    # subbands in three directions(horizontal,vertical,diagonal)
    subBands = defaultdict(list)

    # 1.DWT
    for i in range(k):
        U0 = symfilterV(X0, H0, 5)
        U1 = symfilterV(X0, H1, 3)
        V0, V1 = DownSamplingHorizontal(U0, U1)
        B1 = symfilterH(V0, H0, 5)
        B2 = symfilterH(V0, H1, 3)
        B3 = symfilterH(V1, H0, 5)
        B4 = symfilterH(V1, H1, 3)

        LL, LH = DownSamplingVertical(B1, B2) 
        HL, HH = DownSamplingVertical(B3, B4) 

        X0 = LL
        subBands["HL"].insert(0, HL)
        subBands["LH"].insert(0, LH)
        subBands["HH"].insert(0, HH)

    # 2.Quantization
    # LL_Quantized = Quantizer.Quantization(LL, 1)
    for direction in subBands.keys():
        for i in range(0,3):
            subBands[direction][i] = Quantizer.Quantization(subBands[direction][i], 1)
    # zero_cnt = np.where(LL_Quantized, 0, 1)
    # print("percent of zero is {:.1f}%".format(100 * np.sum(zero_cnt) / LL_Quantized.size))

    # 3.Encoder-RLE&Huffman(only process SymbolStream)
    # prediction_item, LL_Symbol_seq, LL_Binary_seq = RLE(subBands["LH"], subBands, "LH")
    LL_Symbol_seq, LL_Binary_seq = RLE(subBands["LH"][0], subBands, "LH") # img->RLE
    Huffman_Root, HuffmanEncodedStream = HuffmanEncode(LL_Symbol_seq)

    # 4.Decoder 
    HuffmanDecodeStream = HuffmanDecode(Huffman_Root, HuffmanEncodedStream) # HuffmanBitStream->SymbolStream
    Decode_Symbol_seq = Decode(HuffmanDecodeStream, LL_Binary_seq) # RLE->OneDimList
    Decode_SubBand_1 = np.array(Decode_Symbol_seq[0:4096], dtype=np.int32).reshape(64,64) # OneDimList->img
    # Decode_Symbol_seq[1:] += prediction_item
    # Decode_Symbol_seq = np.array(Decode_Symbol_seq, dtype=np.int32).reshape(64, 64)

    print(np.array_equal(Decode_SubBand_1, subBands["LH"][0]))


    # 5.DeQuantization
    # LL = Quantizer.DeQuantization(LL, 1)

    # # 6.IDWT
    # for i in range(k):
    #     D1 = upsampleVertical(LL) 
    #     D2 = upsampleVertical(subBands["LH"][i])
    #     # D1[1::2] = D2[::2]
    #     D3 = upsampleVertical(subBands["HL"][i]) 
    #     D4 = upsampleVertical(subBands["HH"][i]) 
    #     C1 = symfilterH(D1, G0, 3)
    #     C2 = symfilterH(D2, G1, 5)
    #     C3 = symfilterH(D3, G0, 3)
    #     C4 = symfilterH(D4, G1, 5)

    #     W0 = upsampleHorizontal(C1,C2)
    #     W1 = upsampleHorizontal(C3,C4)

    #     Y0 = symfilterV(W0, G0, 3)
    #     Y1 = symfilterV(W1, G1, 5)
    #     Y = Y0 + Y1

    #     LL = Y

    #     # Y = np.where(Y < X.max(), Y, X.max())
    #     # Y = np.where(Y > X.min(), Y, X.min())
    #     # Y = (Y - Y.min()) / (Y.max() - Y.min()) * (X.max() - X.min())

    # plt.imshow(Y, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    # plt.show()
    # print(PSNR(X, Y))

if __name__ == "__main__":
    main(3)
