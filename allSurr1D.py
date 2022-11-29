import numpy as np
import os
import re
from analyse.routines import *
from pltSSsur import pltSSsur

def allSurr1D(data_dir = 'data', score_file = 'ARScore.txt', *,save_as):

    valid = {'csv', 'pkl'}
    if save_as not in valid:
        raise ValueError(f"Invalid value for argument 'save_as'! Valid value: {valid}")

    nClass = [0, 1, 2, 3] # classes

    # proportion - to prevent one class overshadows other classes
    # the higher the no.of sample in the class, the lower the value of nSur
    nSur = [12, 6, 1, 1] #TODO <-- manually tuned to auto
    fold_no = 30 # how many times the data is augmented from one sample
    
    # no. of surrogates depend on score
    nSur = np.dot(nSur, fold_no)

    # set working directory, clear content if not empty
    work_dir_path = set_work_dir("wrkdir")

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
        


if __name__ == '__main__':
    allSurr1D(save_as="csv")