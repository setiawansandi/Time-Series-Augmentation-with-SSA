import os
from numpy import mean, power, argmin
from math import log

def set_dataf(_file_name, is_csv):
    '''Getting and setting data path

    If the arguement _file_name is null, prompt for name
    If the argument is_csv is True, use .csv file extension

    Returns
    -------
        String: string of the path to the file
        String: string of file name
    '''

    if _file_name == '':
        _file_name = input("Enter file name: ")
    
    if (is_csv):
        _file_name += '.csv'
    else:
        _file_name += '.bin'

    _file_path = os.path.dirname(os.path.realpath(__file__))

    # os.path.join will concatenate the path.
    # os.path.abspath will interprate os.pardir as 
    # going up by one directory + return abs path.
    _file_path = os.path.abspath(os.path.join(_file_path, os.pardir, "data"))

    return _file_path, _file_name



def read_ARAT(): #TODO
    '''
    read binary data
    '''
    readOk = False


    pass



def get_min(V):
    # estimate RDE per Braun given sorted eigenvalues in V
    V0 = V - mean(V)
    N = len(V)
    nlgd = []

    for d in range(N-1): # length of data
        sig1 = sum(power(V0[0:d+1], 2)) / (d+1)
        sig2 = sum(power(V0[d+1:], 2)) / (N-d-1)
        res = log(sig1 ** 2) * (d+1) / N + log(sig2 ** 2) * (N-d-1) / N
        nlgd.append(res)

    return argmin(nlgd)
    
    

