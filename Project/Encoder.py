import numpy as np

# get the size of each element in list
def get_size(val:int):
    if(val <= -512 or val >= 512): return "j" #10
    if(val <= -256 or val >= 256): return "i" #9
    if(val <= -128 or val >= 128): return "h" #8
    if(val <= -64 or val >= 64): return "g" #7
    if(val <= -32 or val >= 32): return "f" #6
    if(val <= -16 or val >= 16): return "e" #5
    if(val <= -8 or val >= 8): return "d" #4
    if(val <= -4 or val >= 4): return "c" #3
    if(val <= -2 or val >= 2): return "b" #2
    if(val == -1 or val == 1): return "a" #1
# get the element index in corresponding size
def size_idx(val:int, size:str):
    power = ord(size) - ord("a") + 1
    init_val = -1 * np.power(2, power) + 1 if val < 0 else np.power(2, power) - 1
    idx = val - init_val if val < 0 else np.power(2, power) - (init_val - val) - 1
    return bin(idx)[2:]

def EZW(currentPixel:int, scale:int, scaleIdx:int, subBands:list, direction:str):
    ## do EZW operation
    row = currentPixel // scale # get the row of current element
    col = currentPixel % scale # get the col of current element
    multiplier = 2
    for idx in range(scaleIdx,3):
        ZTR = np.sum(np.where(subBands[direction][idx][row*multiplier:(row+1)*multiplier, col*multiplier:(col+1)*multiplier], 1, 0)) # small block -> big blcok
        if ZTR == 0: # current block all equal to 0, go down
            multiplier *= 2
            continue
        else: # current block exist non-zero element->isolated zero
            return "k" # 0
    return "l" # ZTR

# RLE Encoding
def RLE(img:np.ndarray, subBands:list, flag:str):
    # subbands: HL_list, LH_list, HH_list
    encoded_seq = [] # encoded bit stream
    Binary_seq = [] # Amplitude bit stream

    if flag == "Lowest":
        img_OneDim = img.flatten() 
        # DC prediction:
        img_OneDim[1:] = img_OneDim[1:] - img_OneDim[0]
        for i in range(len(img_OneDim)):
            if img_OneDim[i] != 0 : # NZ
                current_size = get_size(img_OneDim[i])
                encoded_seq.append(current_size)
                Binary_seq.append(size_idx(img_OneDim[i], current_size))
                # Binary_seq.append(bin(img_OneDim[i])[2:])
            else: # Zero
                encoded_seq.append("k")
    else: # 2.other subbands:64,128,256
        for scaleIdx in range(0,3): # two children in the same direction 
            scale = img.shape[0]
            img_OneDim = img.flatten()
            for i in range(len(img_OneDim)): # one parent
                if img_OneDim[i] != 0: # NZ
                    current_size = get_size(img_OneDim[i])
                    encoded_seq.append(current_size)
                    Binary_seq.append(size_idx(img_OneDim[i], current_size))
                    # Binary_seq.append(bin(img_OneDim[i])[2:])
                else: # accur zero, judge ZTR
                    if scaleIdx != 2:
                        symbol = EZW(i, scale, scaleIdx+1, subBands, flag)
                        encoded_seq.append(symbol)
                        # Binary_seq.append(bin(symbol)) # this line need to be optimized(ZTR how to encode)
                    else: encoded_seq.append("k")
            # parent image is scaned, go to children image
            if scaleIdx != 2 : img = subBands[flag][scaleIdx+1]
    encoded_seq = "".join(encoded_seq)
    Binary_seq = "".join(Binary_seq)
    return encoded_seq, Binary_seq

        # # sample each 16 element
        # if (i+1) % 3 == 0 and (i+1) != len(img_OneDim):
        #     if(img_OneDim[i] == 0):
        #         encoded_seq.append((Run_count, 0))
        #     else:
        #         encoded_seq.append(((Run_count, get_size(img_OneDim[i])), bin(img_OneDim[i])[2:]))
        #         Run_count = 0
        #     continue

        # # if current element is zero, increasing count
        # if img_OneDim[i] == 0:
        #     Run_count += 1
        # # if current element is not zero, push it into the bitstream list
        # else:
        #     encoded_seq.append(((Run_count, get_size(img_OneDim[i])), bin(img_OneDim[i])[2:]))
        #     Run_count = 0
        # if i == len(img_OneDim)-1 and Run_count != 0:
        #     encoded_seq.append("EOB")