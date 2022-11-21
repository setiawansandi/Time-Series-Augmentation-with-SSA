import numpy as np

fe = '.BIN' # file extension
sfe = '.csv' # surrogate file extension

nClass = np.array([0, 1, 2, 3])
nSur = [12, 6, 1, 1]
fold_no = 30

# surrogates depend on score 0/1/2/3, np.dot = scalar multiplication
nSur = np.dot(nSur, fold_no)



variable = nSur
print(variable)
print(type(variable))