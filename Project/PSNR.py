import numpy as np

def PSNR(img1, img2):
    mse = np.sum((img1.astype(float) - img2.astype(float)) ** 2) / (float(img1.shape[1] * img1.shape[0]))
    print("MSE = ",mse)
    psnr = 10 * np.log10(255 ** 2 / mse)

    return psnr

