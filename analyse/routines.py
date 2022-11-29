import os
from numpy import mean, power, argmin
from math import log
from pathlib import Path

def set_dataf(file_name, is_csv):
    '''Getting and setting data path

    If the arguement _file_name is null, prompt for name
    If the argument is_csv is True, use .csv file extension

    Returns
    -------
        file_path: string of the path to the file
        String: string of file name
    '''

    file_path = os.path.dirname(os.path.realpath(__file__))

    # os.path.join will concatenate the path.
    # os.path.abspath will interprate os.pardir as 
    # going up by one directory + return abs path.
    file_path = os.path.abspath(os.path.join(file_path, os.pardir, "data"))

    return file_path, file_name


def set_data_file(file_name):
    '''set data path

    Syntax: [file_abs_path] = set_data_file(file_name)

    Returns
    -------
        file_abs_path - absolute path to the data file
    '''

    current_path = os.path.dirname(os.path.realpath(__file__))

    # os.path.join will concatenate the path.
    # os.path.abspath will interprate os.pardir as 
    # going up by one directory + return abs path.
    file_abs_path = os.path.abspath(os.path.join(current_path, os.pardir, "data", file_name))

    return file_abs_path



def read_BIN(): #TODO
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
    

    
def set_work_dir(dir_name):
    ''' Create working directory

    Syntax: [work_dir_path] = set_work_dir(drv)

    Input: dir_name - directory name

    Returns
    -------
    work_dir_path - path to newly created working directory
    
    '''

    # get current file (routines.py) path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # get relative path to parent dir + join with work dir name
    work_dir_path = os.path.abspath(os.path.join(current_dir, os.pardir, dir_name))

    # create the directory
    try:
        # os.makedirs() method will raise an OSError if the directory
        # to be created already exists. But It can be suppressed by
        # setting the value of a parameter exist_ok as True
        os.makedirs(work_dir_path, exist_ok=True)
        print(f'[INFO] Directory {work_dir_path} is created successfully!')
    except OSError as error:
        print(f'[ERROR] Directory {work_dir_path} can\'t be created')
    
    return work_dir_path



def delete_work_dir(work_dir_path):
    pass
