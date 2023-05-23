import numpy as np

x = [[1,2,3,4,5], [2,3,4,5,6], [3,4,5,6,7]]
x = np.array(x)
x = x.transpose()
print(x)
x = x.transpose()
x = x.tolist()
print(x)