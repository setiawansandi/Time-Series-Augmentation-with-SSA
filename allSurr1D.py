import numpy as np
import os
import re
import shutil
from analyse.routines import *
from pltSSsur import pltSSsur

def allSurr1D(*, data_dir, score_file, save_as, nSur, fold_no):
    ''' Generate surrogate data for all files in data set

    Input:  data_dir - &emsp;&emsp;- data directory
          score_file - score file containing which class the data belong to
             save_as - save output as csv or pickle
                nSur - proportion of surrogate data to be generated (to balance data distribution)
             fold_no - how much the data is going to augmented (x fold)
    
    Returns:
        .csv files in wrkdir
        or
        .pkl file
    '''

    valid = {'csv', 'pkl'}
    if save_as not in valid:
        raise ValueError(f"Invalid value for argument 'save_as'! Valid value: {valid}")
    
    # no. of surrogates depend on score
    nSur = np.dot(nSur, fold_no)

    # delete directory including its content
    shutil.rmtree(r'wrkdir') 
    # set working directory
    work_dir_path = set_work_dir(r"wrkdir")

    # get the score from txt file
    data_score = dict()
    with open(os.path.join(data_dir,score_file)) as score:
        for line in score.readlines():
            data_score[line.split()[0]] = int(line.split()[1])

    for filename in os.listdir(data_dir):

        # regex expression to get sample name [no number]
        nName = re.split('_|\.|\s|-|\)|\(',filename)[0] # split at given symbol
        
        try:
            pscore = data_score[nName] # get score given
        except: continue

        ds_indx = 0 # surr dataset count
        for surrnum in range(nSur[pscore]):
            # generate surrogate
            try:
                res = pltSSsur(filename, data_dir_path=data_dir)
            except: break

            # save syntensized data
            # print(f'[INFO] [{surrnum}] Now at {filename}')
            if save_as == 'csv':
                # construct surrogate file name
                surr_file = filename.split(".")[0]+"_S"+str(surrnum)+"."+filename.split(".")[1]
                file_path = os.path.join(work_dir_path, str(pscore), surr_file)
                save_as_csv(res.T, file_path)
            elif save_as == 'pkl':
                save_as_pickle() #TODO
            ds_indx += 1

        print(f'[INFO] {ds_indx} surrogate data generated from {filename}')
        