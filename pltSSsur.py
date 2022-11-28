import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import sys

from analyse.routines import *
from analyse.ssa import *
from analyse.surrog import *


def pltSSsur(arat_file='', is_csv = True):
    # TODO remove
    arat_file = 'P02_TS_2'

    numR=20;        # how many reconstructed to view - 5
    numComp=3;      # how many components x/y/z
    numFreq=3;      # how many frequency domain values
    M = 17          # embedding dimension
    plot_ok = True if arat_file == '' else False
    EVbp = []

    # ====================== Read file ===========================

    # get path and add file extension
    afp, arat_file = set_dataf(arat_file, is_csv)

    arat_file_path = os.path.join(afp, arat_file)

    # check if file exist in dir
    if not os.path.isfile(arat_file_path):
        raise Exception(f'{arat_file} does not exist!')
    
    if is_csv:
        # read csv files and store data in numpy array
        accel = np.genfromtxt(arat_file_path, delimiter=',')
        accel = accel.transpose() # a * b -> b * a
        data_len = accel.shape[1] # get length of data

    else: # if binary file
        # resAll = np.zeros((numComp, numR, numFreq, 1))
        read_ARAT() #TODO read bin
    
    
    # ======================== Generating ============================

    # create array of all zeros with indicated dimension
    surrdata = np.zeros((numComp,data_len)); 
    
    # loop over the components of signal
    for comp in range(numComp):
        # time and frequency plot for 3 components of acceleration
        plotdata = accel[comp,:];   # get one component of data

        if plot_ok:
            #TODO function to plot
            pass

        # Eigenfunctions, Variances,   principAl components, Reconstructed, Covariance
        # Eigenvectors,   EigenValues, principAl components, Reconstructed, Covariance
        E, V, A, R, C = ssa(plotdata, M)

        EVbp.append(get_min(V)) # eigenvalue breakpoint use Braun's RDE
        
        wavsig = np.zeros((R.shape[0]))
        wavnoise = wavsig.copy()

        # add all reconstructed waves up to breakpoint - gives signal
        for r in range(EVbp[comp]+1):
            wavsig = wavsig + R[:,r]

        # after that is noise component
        for r in range ((EVbp[comp]+1), len(V)):
             wavnoise = wavnoise+R[:,r]

        # Breitenberger's code removes mean so put back as a filtered signal
        wavsigf = wavsig + np.mean(accel[comp,:]);
        
        # surrogate the noise
        wavnoisur = aaft(wavnoise,1); # generate ONE AAFT surrogate     # uncomment for ssa & surr
        
        pass
    
    

    

    
    

if __name__ == '__main__':
    pltSSsur()
