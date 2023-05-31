#coding=gbk
import matplotlib.pyplot as plt
import numpy as np
from symfilterV import symfilterV
from symfilterH import symfilterH
from DownSamplingHorizontal import DownSamplingHorizontal
from DownSamplingVertical import DownSamplingVertical
import upsamleHorizontal
import upsamleVertical
from PSNR import PSNR
import Quantizer
from collections import defaultdict
from Encoder import RLE
from Decoder import Decode
from HuffmanEncode import HuffmanEncode, HuffmanDecode, Huffman_Codebook
import package, time

## filter
H0 = [-1/8, 1/4, 3/4, 1/4, -1/8]
H1 = [-1/2, 1, -1/2]
G0 = [1/2, 1, 1/2]
G1 = [-1/8, -1/4, 3/4, -1/4, -1/8]


def main(k, StepSize):
    # load data
    lena = np.fromfile('image1.512', dtype=np.uint8)
    lena = lena.reshape(512, 512)


    X = lena.copy().astype(np.float32)
    X0 = X

    # subbands in three directions(horizontal,vertical,diagonal)
    subBands = defaultdict(list)
    RootNode = defaultdict(list)
    Scale_Huffman = defaultdict(list)
    LenofHuffman = defaultdict(list)
    Scale_Binary = defaultdict(list)
    LenofBinary = defaultdict(list)

    start = time.time()
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

#####################################################################################################################
    # 2.Quantization
    # for LL
    LL_Quantized = Quantizer.Quantization(LL, StepSize)
    # for subbands
    for direction in subBands.keys():
        for i in range(k):
            subBands[direction][i] = Quantizer.Quantization(subBands[direction][i], StepSize)
            # zero_cnt = np.where(subBands[direction][i], 0, 1)
            # print("percent of zero of {}'s {} scale is {:.1f}%".format(direction, i+1, 100 * np.sum(zero_cnt) / subBands[direction][i].size))
#####################################################################################################################


#####################################################################################################################
    # 3.Encoder-RLE&Huffman(only process SymbolStream)
    # for LL
    prediction_item, LL_Symbol_seq, LL_Binary_seq = RLE(LL_Quantized, subBands, "LL", k) # img->RLE
    LL_HuffmanEncodedStream, RootNode["LL"] = HuffmanEncode(LL_Symbol_seq)
    LL_tobeTransmit = [LL_HuffmanEncodedStream, LL_Binary_seq] # ***noneed to transmit codebook(Root_Node)***
    # for subbands
    for direction in subBands.keys():
        Scale_Huffman[direction], RootNode[direction], LenofHuffman[direction], Scale_Binary[direction], LenofBinary[direction] = RLE(subBands[direction][0], subBands, direction, k)
        # DesubBands[direction].append(temp_Symbol), DesubBands[direction].append(temp_BitStream)
        # DesubBands[direction][0], RootNode[direction], Length[direction] = HuffmanEncode(DesubBands[direction][0])
# #####################################################################################################################

    ## Packing
    LLHuffmanLen, LLBinaryLen = package.PackingLL(LL_tobeTransmit)
    HuffmansubBandsLen, BinarysubBandsLen= package.PackingSubBands(Scale_Huffman, Scale_Binary, k)
    package.PackingRoot(RootNode)
    package.PackingLen(LenofHuffman, LenofBinary, LLHuffmanLen, LLBinaryLen, HuffmansubBandsLen, BinarysubBandsLen)

    ## Socket

    
    ## UnPacking
    DeRoot = package.UnPacking("HuffmanRoot.bin")
    DeLen = package.UnPacking("Len.bin")
    BisubBandsHuffman = package.UnPackingDecimal2Bin("SubBandsHuffman.bin", DeLen[4])
    BisubBandsBinary = package.UnPackingDecimal2Bin("SubBandsBitStream.bin", DeLen[5])
    DesubBands = package.UnPackingSubBands(BisubBandsHuffman, DeLen[0], k)
    DesubBandsBinary = package.UnPackingSubBands(BisubBandsBinary, DeLen[1], k)
    DeLLHuffman = package.UnPackingDecimal2Bin("LLHuffman.bin", DeLen[2])
    DeLLBinary = package.UnPackingDecimal2Bin("LLBinary.bin", DeLen[3])

# #####################################################################################################################
    # 4.Decoder 
    # for LL
    size = 512 // np.power(2, k)
    LLHuffmanDecodeStream = HuffmanDecode(DeLLHuffman, DeRoot["LL"]) # HuffmanBitStream->SymbolStream
    LL_Decode_Symbol = Decode(LLHuffmanDecodeStream, DeLLBinary) # RLE->OneDimList
    LL_Decode_Symbol[1:] += prediction_item
    LL_Decode_Symbol = np.array(LL_Decode_Symbol, dtype=np.float32).reshape(size, size) # OneDimList->img
    # for subands
    for direction in DesubBands.keys():
        size = 512 // np.power(2, k)
        for i in range(k):
            DesubBands[direction][i] = HuffmanDecode(DesubBands[direction][i], RootNode[direction][i])
            DesubBands[direction][i] = Decode(DesubBands[direction][i], DesubBandsBinary[direction][i])
            DesubBands[direction][i] = np.array(DesubBands[direction][i], dtype=np.float32).reshape(size,size)
            size *= 2
# #####################################################################################################################


# #####################################################################################################################
    # 5.DeQuantization
    # for LL
    LL = Quantizer.DeQuantization(LL_Decode_Symbol, StepSize)
    # for subBands
    for direction in DesubBands.keys():
        for i in range(k):
            DesubBands[direction][i] = Quantizer.DeQuantization(DesubBands[direction][i], StepSize)
# #####################################################################################################################

# #####################################################################################################################
    # 6.IDWTs
    for i in range(k):
        D1 = upsamleVertical.upsampleVerticalLP(LL) 
        D2 = upsamleVertical.upsampleVerticalHP(DesubBands["LH"][i])
        D3 = upsamleVertical.upsampleVerticalLP(DesubBands["HL"][i]) 
        D4 = upsamleVertical.upsampleVerticalHP(DesubBands["HH"][i]) 
        C1 = symfilterH(D1, G0, 3)
        C2 = symfilterH(D2, G1, 5)
        C3 = symfilterH(D3, G0, 3)
        C4 = symfilterH(D4, G1, 5)

        W0 = upsamleHorizontal.upsampleHorizontalLP(C1+C2)
        W1 = upsamleHorizontal.upsampleHorizontalHP(C3+C4)

        Y0 = symfilterV(W0, G0, 3)
        Y1 = symfilterV(W1, G1, 5)
        Y = Y0 + Y1

        LL = Y

    end = time.time()
    print("Total time is {:.5f}s".format(end - start))
    print(PSNR(X, Y))
    plt.subplot(121), plt.imshow(X, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(Y, 'gray', vmin=0, vmax=255), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == "__main__":
    main(5, 10)
