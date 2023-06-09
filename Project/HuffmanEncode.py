#coding=gbk
import numpy as np
from queue import PriorityQueue
from collections import Counter

Huffman_Codebook = {} # 全局变量哈夫曼编码字典{key:code}

# 哈夫曼树的节点class
class HuffmanNode(object):
    def __init__(self, weight, key=None, symbol='', left_Child=None, right_Child=None):
        # 哈夫曼树的节点的初始化
        
        self.weight = weight # weight：权值，即频率
        self.key = key # key：叶子节点的元素
        self.left_Child = left_Child # left_Child：左子节点
        self.right_Child = right_Child # right_Child：右子节点
        if symbol != '':
            return False
        else:
            self.symbol = symbol # symbol：叶子节点的哈夫曼编码，初始化为空字符串


    def __ge__(self, other) -> bool:
        # 比较前一个HuffmanNode的weight值是否大于等于后一个
        return self.weight >= other.weight

    def __lt__(self, other) -> bool:
        # 比较前一个HuffmanNode的weight值是否小于后一个
        return self.weight < other.weight


def CreateHuffmanTree(file : dict) -> HuffmanNode:
    # 自底向上构建哈夫曼树
    # file：输入字典文件
    # HuffmanNode：哈夫曼树的root节点

    # 使用优先级队列方便进行频率权值的排序
    q = PriorityQueue()

    # 根据传入的键&值创建哈夫曼节点并存入队列
    for key, value in file: 
        # 存入哈夫曼树的叶子节点
        q.put(HuffmanNode(weight=value, key=key))

    # 进行判断，看当前队列是否到达root节点
    while q.qsize() > 1:
        # 取出队列中最小的两个节点(左子节点权值<右子节点权值)，同时将这两个节点从队列中剔除
        l_Node , r_Node = q.get(), q.get()
        # 由两个子节点创建父节点，对于父节点不赋予元素值
        Node = HuffmanNode(weight=l_Node.weight + r_Node.weight, left_Child=l_Node, right_Child=r_Node)
        # 然后将父节点存入队列，循环往复直至构建整个哈夫曼树
        q.put(Node)

    # 若当前队列只剩下root节点，则进行返回操作
    return q.get()

def TreeTraversal(root_Node, symbol=''):
    # 遍历哈夫曼树，获取每个叶子节点元素的哈夫曼编码，并进行保存
    # root_Node：哈夫曼树的根节点
    # symbol：对哈夫曼树进行递归时对其上所有节点进行编码，为'0'或'1'

    global Huffman_Codebook

    # 判断节点是否为HuffmanNode，因为叶子节点的子节点是None
    # "isinstance(a,b)"：若object a是class b的实例或子类的实例，返回True，否则为False
    if isinstance(root_Node, HuffmanNode):
        # 进行编码操作，改变每个子树根节点的哈夫曼编码
        root_Node.symbol += symbol
        # 判断是否到达叶子节点
        if root_Node.key != None:
            # 记录叶子节点的编码
            Huffman_Codebook[root_Node.key] = root_Node.symbol

        # 访问左子树，并在根节点基础上赋'0'
        TreeTraversal(root_Node.left_Child, symbol=root_Node.symbol + '0')
        # 访问右子树，并在根节点基础上赋'1'
        TreeTraversal(root_Node.right_Child, symbol=root_Node.symbol + '1')

def encoder(encoded_file:np.ndarray, codebook:dict):
    # 用codebook对文件进行编码-编码器
    # endoded_file：原始文件数据
    # codebook：编码字典，dict={key:code}

    file_encode = ''
    # assert len(encoded_file.shape) == 1, 'input file must a vector'
    # for element_line in encoded_file: # 遍历输入文件会先取出每一行，并将每一行作为一个整体字符串
    #     for element in element_line: # 再向下遍历一层才能取出每一行整体字符串中的单个字符串
    #         file_encode += codebook[element]
    for key in encoded_file:
        file_encode += codebook[key]
        # print(value)  
    return file_encode

# write
# read

def decoder(bitStream_encode:str, huffman_tree_root:HuffmanNode):
    # 解码器
    # img_encode：哈夫曼编码数据，只包含"0"&"1"
    # huffman_tree_root：哈夫曼树根节点
    # return 原图像数据展开的向量
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

# def decoder(img_encode: str, encode_dict: dict):
#     '''
#     另外一种解码策略是先遍历一遍哈夫曼树得到所有叶子节点编码对应的元素，可以保存在字典中，再对字符串的子串逐个与字典的键进行比对，就得到相应的元素是什么。
#     :param img_encode: 哈夫曼编码数据，只包含'0'和'1'的字符串
#     :param encode_dict: 编码字典dict={element:code}
#     :return: 原始图像数据展开的向量
#     '''
#     bitStream_decode = []
#     decode_dict = {}
#     # 构造一个key-value互换的字典，i.e. dict={code:element}，后边方便使用
#     for k, v in encode_dict.items():
#         decode_dict[v] = k
#     # s用来记录当前字符串的访问位置，相当于一个指针
#     s = 0
#     # 只要没有访问到最后
#     while len(img_encode) > s + 1:
#         # 遍历字典中每一个键code
#         for k in decode_dict.keys():
#             # 如果当前的code字符串与编码字符串前k个字符相同，k表示code字符串的长度，那么就可以确定这k个编码对应的元素是什么
#             if k == img_encode[s:s + len(k)]:
#                 bitStream_decode.append(decode_dict[k])
#                 # 指针移动k个单位
#                 s += len(k)
#                 # 如果已经找到了相应的编码了，就可以找下一个了
#                 break
#     bitStream_decode = "".join(bitStream_decode)
#     return bitStream_decode


def HuffmanEncode(original_seq:str):
    ### 1.Preprocessing
    # load file(SymbolStream)
    frequency_dict = Counter(original_seq).items()
    # create HuffmanTree and get encode of leaf
    Huffman_root_Node = CreateHuffmanTree(frequency_dict)
    TreeTraversal(Huffman_root_Node)
    # print("哈夫曼字典为: {}".format(Huffman_Codebook))

    ### 2.Encoding
    ###################################
    # 保存字符串文件
    # SymbolStream -> HuffmanBitStream
    HuffmanBitStream = encoder(original_seq, Huffman_Codebook)
    # print("Huffman编码后的bitStream为: {}".format(HuffmanBitStream))
    # with open("encoded.txt", 'w') as f:
    #     f.write(endoced_file) # 将编码后的字符串保存为txt文件
    ###################################

    return HuffmanBitStream, Huffman_root_Node

    
### 3.Decoding
def HuffmanDecode(EncodedBitStream:str, Huffman_Root:HuffmanNode):
    HuffmanDecodeStream = decoder(EncodedBitStream, Huffman_Root)

    return HuffmanDecodeStream