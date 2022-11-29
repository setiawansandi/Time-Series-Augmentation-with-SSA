import numpy as np
import os
import matplotlib.pyplot as plt

from analyse.routines import *
from analyse.ssa import *
from analyse.surrog import *


def pltSSsur(file_name, *, data_dir_path, numComp = 3, plot_ok = False):
    ''' perform SSA decomposition

    Syntax: [surrdata] = pltSSsur(file_name, is_csv, numComp)

    perform SSA decomposition of signals from a file of ARAT data
    and do reconstruction based on significant eigenvalues
    leave "noise" to be randomized by surrogate

    INPUT:   file_name - file name of the sample data
                is_csv - bool, 'True' if the sample data file is csv
               numComp - number of components
               plot_ok - bool, 'True' will return both file data and surrdata

    OUTPUT:   surrdata - surrogate data (matrix of 'numComp' columns)

    TL 2022
    '''
    
    numR=20;        # how many reconstructed to view - 5
    numComp=numComp;# how many components x/y/z
    numFreq=3;      # how many frequency domain values
    M = 17          # embedding dimension
    EVbp = []

    # ====================== Read file ===========================

    # get file path
    data_file_path = set_data_file(file_name, data_dir_path)

    # check if file exist in dir
    if not os.path.isfile(data_file_path):
        raise Exception(f'{file_name} does not exist!'
            ' Check if file name or extension is correct')
    
    fe = os.path.splitext(file_name)[-1].lower() # get file extension
    if fe == '.csv' or fe == '.txt':
        # read and store the data in a numpy array
        accel = np.genfromtxt(data_file_path, delimiter=',')
        accel = accel.transpose() # a * b -> b * a
        data_len = accel.shape[1] # get length of data

    elif fe == '.bin':
        raise Exception("method to read .bin is not implemented")
        '''accel = read_BIN()''' #TODO read bin
    else:
        raise Exception(f"Invalid file format! {fe} file is not accepted")
    
    # ======================== Generating ============================

    # create array of all zeros with indicated dimension
    surrdata = np.zeros((numComp,data_len)); 
    
    # loop over the components of signal
    for comp in range(numComp):
        # time and frequency plot for 3 components of acceleration
        plotdata = accel[comp,:];   # get one component of data

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
        '''wavnoisur = aaft(plotdata,1)''' # use whole waveform for comparison

        # add back to original
        wavssasur = np.add(wavsigf, wavnoisur) # uncomment for ssa & surr
        '''wavssasur = wavnoisur'''
        
        surrdata[comp,:] = wavssasur;
    
    if plot_ok:
        return accel, surrdata
    
    return surrdata

    
if __name__ == '__main__':
    _fn = input('Enter file name: ')
    if _fn == '': _fn = 'P02_TS_2.csv' # for testing
    accel, surrdata = pltSSsur(_fn, numComp=3, plot_ok=True)