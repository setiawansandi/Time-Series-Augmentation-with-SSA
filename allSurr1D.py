import numpy as np
import os
import re
from analyse.routines import set_work_dir, delete_work_dir
from pltSSsur import pltSSsur

def allSurr1D(data_dir = 'data', score_file = 'ARScore.txt', *,save_as):

    valid = {'csv', 'pkl'}
    if save_as not in valid:
        raise ValueError(f"Invalid value for argument 'save_as'! Valid value: {valid}")

    fe = '.bin'
    sfe = '.csv'

    nClass = [0, 1, 2, 3] # classes

    # proportion - to prevent one class overshadows other classes
    # the higher the no.of sample in the class, the lower the value of nSur
    nSur = [12, 6, 1, 1] #TODO <-- manually tuned to auto
    fold_no = 30 # how many times the data is augmented from one sample
    nSur_folded = np.dot(nSur, fold_no)
    
    # surrogates depend on score, np.dot = scalar multiplication
    nSur = np.dot(nSur, fold_no)

    work_dir_path = set_work_dir("wrkdir") # set working directory

    data_score = dict()
    with open(os.path.join(data_dir,score_file)) as score:
        for line in score.readlines():
            data_score[line.split()[0]] = int(line.split()[1])

    for filename in os.listdir(data_dir):

        # regex expression to split at initialised char - to get name
        nName = re.split('_|\.|\s|-|\)|\(',filename)[0]
        
        try:
            pscore = data_score[nName] # get score given
        except: continue

        for surrnum in range(nSur[pscore]):
            res = pltSSsur(filename, data_dir_path=data_dir)




    print(data_score)


        #check if the file name is in the score
        # the last value is the number of trials


    #TODO if pltSSsur return errors, continue


    delete_work_dir(work_dir_path)


if __name__ == '__main__':
    allSurr1D(save_as="pkl")