#coding=gbk
import numpy as np
from queue import PriorityQueue
from collections import Counter

HuffmanTree_Code = {} # ȫ�ֱ��������������ֵ�{key:code}

# ���������Ľڵ�class
class HuffmanNode(object):
    def __init__(self, weight, key=None, symbol='', left_Child=None, right_Child=None):
        # ���������Ľڵ�ĳ�ʼ��
        
        self.weight = weight # weight��Ȩֵ����Ƶ��
        self.key = key # key��Ҷ�ӽڵ��Ԫ��
        self.left_Child = left_Child # left_Child�����ӽڵ�
        self.right_Child = right_Child # right_Child�����ӽڵ�
        if symbol != '':
            return False
        else:
            self.symbol = symbol # symbol��Ҷ�ӽڵ�Ĺ��������룬��ʼ��Ϊ���ַ���


    def __ge__(self, other) -> bool:
        # �Ƚ�ǰһ��HuffmanNode��weightֵ�Ƿ���ڵ��ں�һ��
        return self.weight >= other.weight

    def __lt__(self, other) -> bool:
        # �Ƚ�ǰһ��HuffmanNode��weightֵ�Ƿ�С�ں�һ��
        return self.weight < other.weight


def CreateHuffmanTree(file : dict) -> HuffmanNode:
    # �Ե����Ϲ�����������
    # file�������ֵ��ļ�
    # HuffmanNode������������root�ڵ�

    # ʹ�����ȼ����з������Ƶ��Ȩֵ������
    q = PriorityQueue()

    # ���ݴ���ļ�&ֵ�����������ڵ㲢�������
    for key, value in file: 
        # �������������Ҷ�ӽڵ�
        q.put(HuffmanNode(weight=value, key=key))

    # �����жϣ�����ǰ�����Ƿ񵽴�root�ڵ�
    while q.qsize() > 1:
        # ȡ����������С�������ڵ�(���ӽڵ�Ȩֵ<���ӽڵ�Ȩֵ)��ͬʱ���������ڵ�Ӷ������޳�
        l_Node , r_Node = q.get(), q.get()
        # �������ӽڵ㴴�����ڵ㣬���ڸ��ڵ㲻����Ԫ��ֵ
        Node = HuffmanNode(weight=l_Node.weight + r_Node.weight, left_Child=l_Node, right_Child=r_Node)
        # Ȼ�󽫸��ڵ������У�ѭ������ֱ������������������
        q.put(Node)

    # ����ǰ����ֻʣ��root�ڵ㣬����з��ز���
    return q.get()

def TreeTraversal(root_Node, symbol=''):
    # ����������������ȡÿ��Ҷ�ӽڵ�Ԫ�صĹ��������룬�����б���
    # root_Node�����������ĸ��ڵ�
    # symbol���Թ����������еݹ�ʱ���������нڵ���б��룬Ϊ'0'��'1'

    global HuffmanTree_Code

    # �жϽڵ��Ƿ�ΪHuffmanNode����ΪҶ�ӽڵ���ӽڵ���None
    # "isinstance(a,b)"����object a��class b��ʵ���������ʵ��������True������ΪFalse
    if isinstance(root_Node, HuffmanNode):
        # ���б���������ı�ÿ���������ڵ�Ĺ���������
        root_Node.symbol += symbol
        # �ж��Ƿ񵽴�Ҷ�ӽڵ�
        if root_Node.key != None:
            # ��¼Ҷ�ӽڵ�ı���
            HuffmanTree_Code[root_Node.key] = root_Node.symbol

        # ���������������ڸ��ڵ�����ϸ�'0'
        TreeTraversal(root_Node.left_Child, symbol=root_Node.symbol + '0')
        # ���������������ڸ��ڵ�����ϸ�'1'
        TreeTraversal(root_Node.right_Child, symbol=root_Node.symbol + '1')

def encoder(encoded_file:np.ndarray, codebook:dict):
    # ��codebook���ļ����б���-������
    # endoded_file��ԭʼ�ļ�����
    # codebook�������ֵ䣬dict={key:code}

    file_encode = ''
    # assert len(encoded_file.shape) == 1, 'input file must a vector'
    # for element_line in encoded_file: # ���������ļ�����ȡ��ÿһ�У�����ÿһ����Ϊһ�������ַ���
    #     for element in element_line: # �����±���һ�����ȡ��ÿһ�������ַ����еĵ����ַ���
    #         file_encode += codebook[element]
    for key in encoded_file:
        file_encode += codebook[key]
        # print(value)  
    return file_encode

# write
# read

def decoder(bitStream_encode:str, huffman_tree_root:HuffmanNode):
    # ������
    # img_encode���������������ݣ�ֻ����"0"&"1"
    # huffman_tree_root�������������ڵ�
    # return ԭͼ������չ��������
    bitStream_decode = []
    root_node = huffman_tree_root

    for code in bitStream_encode:
        # if current code is "0", go left tree
        if code == "0":
            root_node = root_node.left_Child
        # if current code is "1", go right tree
        elif code == "1":
            root_node = root_node.right_Child
        # only leaf's key is not None, determine whether current node is leaf
        if root_node.key != None:
            bitStream_decode.append(root_node.key) # if current node is leaf, record the key
            root_node = huffman_tree_root # access the leaf node, next iteration should start from root of tree

    bitStream_decode = "".join(bitStream_decode)
    return bitStream_decode



def HuffmanEncode(original_seq:str):
    ### 1.Preprocessing
    # load file(SymbolStream)
    frequency_dict = Counter(original_seq).items()
    # create HuffmanTree and get encode of leaf
    Huffman_root_Node = CreateHuffmanTree(frequency_dict)
    TreeTraversal(Huffman_root_Node)
    # print("�������ֵ�Ϊ: {}".format(HuffmanTree_Code))

    ### 2.Encoding
    ###################################
    # �����ַ����ļ�
    # SymbolStream -> HuffmanBitStream
    HuffmanBitStream = encoder(original_seq, HuffmanTree_Code)
    # print("Huffman������bitStreamΪ: {}".format(HuffmanBitStream))
    # with open("encoded.txt", 'w') as f:
    #     f.write(endoced_file) # ���������ַ�������Ϊtxt�ļ�
    ###################################

    return Huffman_root_Node, HuffmanBitStream

    
### 3.Decoding
def HuffmanDecode(Huffman_root:HuffmanNode, EncodedBitStream:str):
    HuffmanDecodeStream = decoder(EncodedBitStream, Huffman_root)

    return HuffmanDecodeStream