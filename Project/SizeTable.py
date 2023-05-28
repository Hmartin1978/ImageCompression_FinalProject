import numpy as np
from collections import defaultdict

sizeTable = defaultdict(list)
sizeTable["a"].append([-1,1])
sizeTable["b"].append([-3,-2,2,3])
sizeTable["c"].append(np.concatenate((np.arange(-7,-3), np.arange(4,8))))
sizeTable["d"].append(np.concatenate((np.arange(-15,-7), np.arange(8,16))))
sizeTable["e"].append(np.concatenate((np.arange(-31,-15), np.arange(16,32))))
sizeTable["f"].append(np.concatenate((np.arange(-63,-31), np.arange(32,64))))
sizeTable["g"].append(np.concatenate((np.arange(-127,-63), np.arange(64,128))))
sizeTable["h"].append(np.concatenate((np.arange(-255,-127), np.arange(128,256))))
sizeTable["i"].append(np.concatenate((np.arange(-511,-255), np.arange(256,512))))
sizeTable["j"].append(np.concatenate((np.arange(-1023,-511), np.arange(512,1024))))