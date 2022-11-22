import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import sys

from analyse.routines import *
from analyse.ssa import *
from analyse.surrog import *


def pltSSsur(arat_file='', is_csv = True):
    # TODO change to args parser
    numR=20;        # how many reconstructed to view - 5
    numComp=3;      # how many components x/y/z
    numFreq=3;      # how many frequency domain values
    M = 17          # embedding dimension
    plot_ok = True if arat_file == '' else False

    # ========================== Read file ===============================

    # get path and add file extension
    afp, arat_file = set_dataf(arat_file, is_csv)

    arat_file_path = os.path.join(afp, arat_file)

    # check if file exist in dir
    if not os.path.isfile(arat_file_path):
        print(f"[INFO] {arat_file} file not found")
        return -1
    
    if is_csv:
        # read csv files and store data in numpy array
        _data = np.genfromtxt(arat_file_path, delimiter=',')
        _data = _data.transpose() # a * b -> b * a
        data_len = _data.shape[1] # get length of data

    else: # if binary file
        # resAll = np.zeros((numComp, numR, numFreq, 1))
        read_ARAT() #TODO read bin
    
    
    # ========================= Generating ==============================

    # create array of all zeros with indicated dimension
    surrdata = np.zeros((numComp,data_len)); 
    
    # loop over the components of signal
    for i in range(numComp):
        # time and frequency plot for 3 components of acceleration
        plotdata = _data[i,:];   # get one component of data

        if plot_ok:
            #TODO function to plot
            pass

        try:
            E, V, A, R, C = ssa(plotdata, M)
        except:
            pass

    
    

    

    
    

if __name__ == '__main__':
    pltSSsur()
