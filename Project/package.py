#coding=gbk
import numpy as np
import pickle
import struct
from collections import defaultdict

Data = []

LLHuffman_path = "LLHuffman.bin"
LLBinary_path = "LLBinary.bin"

HuffmanStream_path = "SubBandsHuffman.bin"
BitStream_path = "SubBandsBitStream.bin"

Root_path = "HuffmanRoot.bin"
Len_path = "Len.bin"

def PackingLL(LLtobeTransmit:list):
    LLHuffman = LLtobeTransmit[0]
    LLBinary = LLtobeTransmit[1]

    LLHuffmanLen = len(LLHuffman)
    LLBinaryLen = len(LLBinary)

    with open(LLHuffman_path, 'wb') as f1:
    # ÿ8��bit���һ��byte
        for i in range(0, len(LLHuffman), 8):
            # ����һ���ֽڵ����ݸ��ݶ����Ʒ���Ϊʮ���Ƶ�����
            img_encode_dec = int(LLHuffman[i:i + 8], 2)
            # ����һ���ֽڵ�ʮ�������ݴ��Ϊһ��unsigned char����ˣ���ʡ�ԣ�
            img_encode_bin = struct.pack('>B', img_encode_dec)
            # д����һ���ֽ�����
            f1.write(img_encode_bin)

    with open(LLBinary_path, 'wb') as f2:
        for i in range(0, len(LLBinary), 8):
            img_encode_dec = int(LLBinary[i:i + 8], 2)
            img_encode_bin = struct.pack('>B', img_encode_dec)
            f2.write(img_encode_bin)

    return LLHuffmanLen, LLBinaryLen

def PackingSubBands(scale_Huffman, scale_Binary, k):
    HuffmanToBeTransmit = []
    BinaryToBeTransmit = []
    
    for direction in scale_Huffman.keys():
        for i in range(k):
            HuffmanToBeTransmit += scale_Huffman[direction][i]
            BinaryToBeTransmit += scale_Binary[direction][i]

    HuffmanToBeTransmit = "".join(HuffmanToBeTransmit)
    BinaryToBeTransmit = "".join(BinaryToBeTransmit)
    LenSubBandHuffman = len(HuffmanToBeTransmit)
    LenSubBandBinary = len(BinaryToBeTransmit)

    with open(HuffmanStream_path, 'wb') as f1:
        for i in range(0, len(HuffmanToBeTransmit), 8):
            img_encode_dec = int(HuffmanToBeTransmit[i:i + 8], 2)
            img_encode_bin = struct.pack('>B', img_encode_dec)
            f1.write(img_encode_bin)

    with open(BitStream_path, 'wb') as f2:
        for i in range(0, len(BinaryToBeTransmit), 8):
            img_encode_dec = int(BinaryToBeTransmit[i:i + 8], 2)
            img_encode_bin = struct.pack('>B', img_encode_dec)
            f2.write(img_encode_bin)

    return LenSubBandHuffman, LenSubBandBinary

def PackingRoot(RootNode):
    with open(Root_path, "wb") as f:
        pickle.dump(RootNode, f)

def PackingLen(LenofHuffman, LenofBinary, LLHuffman, LLBinary, subBandsHuffman, subBandsBinary):
    data = (LenofHuffman, LenofBinary, LLHuffman, LLBinary, subBandsHuffman, subBandsBinary)
    with open(Len_path, "wb") as f:
        pickle.dump(data, f)


def UnPackingDecimal2Bin(BinFile:str, EncodeLen:int):
    '''
    �Ӷ����Ƶı����ļ���ȡ���ݣ��õ�ԭ���ı�����Ϣ��Ϊֻ����'0'��'1'���ַ���
    :param huffman_file: ����ı����ļ�
    :param img_encode_len: ԭʼ����ĳ��ȣ�����Ҫ�������������һ���ֽڶԲ���
    :return: str, ֻ����'0'��'1'�ı����ַ���
    '''
    code_bin_str = ""
    with open(BinFile, 'rb') as f:
        # ���ļ���ȡ����������
        content = f.read()
        # �Ӷ��������ݽ����ʮ�������ݣ�����������ɵ���tuple
        code_dec_tuple = struct.unpack('>' + 'B' * len(content), content)
        for code_dec in code_dec_tuple:
            # ͨ��bin�ѽ�ѹ��ʮ�������ݷ���Ϊ�����Ƶ��ַ����������Ϊ8λ������ᶪʧ��λ��0
            # 0 -> bin() -> '0b0' -> [2:] -> '0' -> zfill(8) -> '00000000'
            code_bin_str += bin(code_dec)[2:].zfill(8)
        # ����ԭʼ�ı��������ܲ���8λ�����浽һ���ֽڵ�ʱ����ڸ�λ�Զ����0����ȡ��ʱ����Ҫȥ������0�������ȡ���ı�����ԭ���ı��볤
        # �����ȡ�ı����ַ�����ԭʼ�����ַ������ȵĲ������ڶ�ȡ�ı����ַ��������һ���ֽڣ�ȥ����λ����Ӧ������0�Ϳ���
        len_diff = len(code_bin_str) - EncodeLen
        # �ڶ�ȡ�ı����ַ������8λȥ����λ�Ķ����0
        code_bin_str = code_bin_str[:-8] + code_bin_str[-(8 - len_diff):]
    return code_bin_str


def UnPackingSubBands(LongHuffmanCode, Len, k):
    SubBands = defaultdict(list)
    start = 0
    for direction in Len.keys():
        for i in range(k):
            length = Len[direction][i]
            SubBands[direction].append(LongHuffmanCode[start:start+length])
            start = start+length

    return SubBands



def UnPacking(file_path):
    with open(file_path, "rb") as file:
        load_Data = pickle.load(file)

    return load_Data

    