import numpy as np
import os

from analyse.routines import *
from analyse.ssa import *
from analyse.surrog import *


def pltSSsur(file_name, *, data_dir_path, numComp = 3, plot_ok = False, R_ok=False):
    ''' perform SSA decomposition, and 
        performing Fourier decomposition on descending eigenvalues (set R_ok to 'True')

    Syntax:                [surr_data] = pltSSsur(file_name, data_dir_path, plot_ok=False)
            [original_data][surr_data] = pltSSsur(file_name, data_dir_path, plot_ok=True)
                       [Reconstructed] = pltSSsur(file_name, data_dir_path, plot_ok=False, R_ok=True)
        [original_data][Reconstructed] = pltSSsur(file_name, data_dir_path, plot_ok=True, R_ok=True)


    perform SSA decomposition of signals from a file of ARAT data
    and do reconstruction based on significant eigenvalues
    leave "noise" to be randomized by surrogate

    INPUT:   file_name - file name of the sample data
               numComp - number of components (columns) in a file
               plot_ok - bool, 'True' will return both sample data and surr_data for plotting
         data_dir_path - path to data folder (can be absolute or relative)

    OUTPUT:   surr_data - generated surrogate data (contains matrix of 'numComp'-columns)
           original_data - (optional) original sample data

    TL 2022
    '''
    
    numR=16;        # how many reconstructed to view - 5
    numComp=numComp;# how many components x/y/z
    numFreq=3;      # how many frequency domain values
    M = 17          # embedding dimension
    EVbp = []
    R_stacked = None

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
        original_data = np.genfromtxt(data_file_path, delimiter=',')
        original_data = original_data.transpose() # a * b -> b * a
        data_len = original_data.shape[1] # get length of data

    elif fe == '.bin':
        raise Exception("method to read .bin is not implemented")
        '''accel = read_BIN()''' #TODO read bin
    else:
        raise ValueError(f"Invalid file format! {fe} file is not accepted")
    
    # ======================== Generating ============================

    # create array of all zeros with indicated dimension
    surr_data = np.zeros((numComp,data_len)); 
    
    # loop over the components of signal
    for comp in range(numComp):
        # time and frequency plot for 3 components of acceleration
        plotdata = original_data[comp,:];   # get one component of data

        # Eigenfunctions, Variances,   principAl components, Reconstructed, Covariance
        # Eigenvectors,   EigenValues, principAl components, Reconstructed, Covariance
        E, V, A, R, C = ssa(plotdata, M)

        if R_ok: # generate reconstructed
            '''w_cor=wcor(R,M)''' # get w correlations between reconstructed #TODO continue the code pltSSAff
            if R_stacked is None:
                R_stacked = np.vstack([ R[np.newaxis,:,:] ])
            else:
                R_stacked = np.vstack([ R_stacked, R[np.newaxis,:,: ]])
            
        else: # generate surrogate instead           
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
            wavsigf = wavsig + np.mean(original_data[comp,:]);
            
            # surrogate the noise
            wavnoisur = aaft(wavnoise,1); # generate ONE AAFT surrogate     # uncomment for ssa & surr
            '''wavnoisur = aaft(plotdata,1)''' # use whole waveform for comparison

            # add back to original
            wavssasur = np.add(wavsigf, wavnoisur) # uncomment for ssa & surr
            '''wavssasur = wavnoisur'''
            
            surr_data[comp,:] = wavssasur;
    
    if plot_ok:
        if R_ok: return original_data, R_stacked
        else: return original_data, surr_data
    else:
        if R_ok: return R_stacked
        else: return surr_data
    

    
if __name__ == '__main__':
    # no input dialog
    # file_data, surr_data = pltSSsur(_fn='p02_ts_2.csv', numComp=3, plot_ok=True, data_dir_path='data')

    # with input dialog
    from screen.input_box import InputBox
    from PyQt5.QtWidgets import QApplication
    import sys

    App = QApplication(sys.argv) # create pyqt5 app
    ib = InputBox(total_entry=3, fe='csv', separator='_') # Input box config
    sys.exit(App.exec()) # start the app