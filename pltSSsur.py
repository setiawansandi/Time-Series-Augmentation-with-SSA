import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import sys

from analyse.routines import *
from analyse.ssa import *
from analyse.surrog import *


def pltSSsur(arat_file='', is_csv = True):
    numR=20;        # how many reconstructed to view - 5
    numComp=3;      # how many components x/y/z
    numFreq=3;      # how many frequency domain values

    # create array of all zeros with indicated dimension
    resAll = np.zeros((numComp, numR, numFreq, 1))

    # get path and add file extension
    afp, arat_file = set_dataf(arat_file, is_csv)

    arat_file_path = os.path.join(afp, arat_file)

    # check if file exist in dir
    if not os.path.isfile(arat_file_path):
        print(f"[INFO] {arat_file} file not found")
        return -1
    
    if is_csv:
        # read csv files and store data in numpy array
        my_data = np.genfromtxt(arat_file_path, delimiter=',')
        my_data = my_data.transpose() # a * b -> b * a
        data_len = my_data.shape[1] # get length of data

        print(data_len)
    

    

    
    

if __name__ == '__main__':
    pltSSsur()
