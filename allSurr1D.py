import os
import re
import shutil
from analyse.routines import *
from pltSSsur import pltSSsur
import logging
import numpy as np

def allSurr1D(*, data_dir, score_file, save_as, nSur=None, fold_no, num_comp, remove_class=[]):
    ''' Generate surrogate data for all files in data set

    Input:  
            data_dir - data directory
          score_file - name of score file containing which class the data belong to
             save_as - output file format (csv/pkl)
                nSur - proportion of surrogate data to be generated (to balance data distribution)
             fold_no - how many times the data is going to augmented (x fold)
             numComp - number of components (columns) in a data file
        remove_class - specify which class to be removed from the output
    
    Returns:
        None (data is stored in wrkdir)
    '''


    # v======================== Initialize ============================v

    logger=logging.getLogger() # log

    valid = {'csv', 'pkl'}
    if save_as.lower() not in valid:
        raise ValueError(f"Invalid value for argument 'save_as'! Valid value: {valid}")
    else:
        sursdata = [] # to store generated surrogate data (2D matrix)
        sursclass = [] # to store which class (score) of the data belong to
        sursfile = [] # to store file names (if save as csv and for sanity checking)

    # get the scores from txt file
    data_score = dict()
    with open(os.path.join(data_dir,score_file)) as score:
        for line in score.readlines():
            data_score[line.split()[0]] = line.split()[1]
    
    # <<< manually set nSur >>>
    if nSur != None:
        # multiple each value to the number of fold
        nSur = {key: value * fold_no for key, value in nSur.items()}

    # <<< automatically set nSur >>>
    else:
        # calculate ratio of sample from each class
        # classes with lower amount of sample will generate more surrogate data
        nSur = dict()
        for filename in os.listdir(data_dir):
            # regex expression to get sample name [no number]
            nName = re.split('_|\.|\s|-|\)|\(',filename)[0] # split at given symbol

            try:
                if data_score[nName] in nSur:
                    nSur[data_score[nName]]+= 1
                else: nSur[data_score[nName]] = 1 
            except Exception as e:
                print(f'{e} file is not valid')
                continue

        # get the max ratio value from the class
        max_value = max(nSur.values())
    
        # multiple each value to the number of fold
        for n_class, value in nSur.items():
            nSur[n_class] = round((max_value / value) * fold_no)
        

    # v======================== Generating ============================v

    for filename in os.listdir(data_dir):

        # regex expression to get sample name [no number]
        nName = re.split('_|\.|\s|-|\)|\(',filename)[0] # split at given symbol
        
        try:
            pscore = data_score[nName] # get score given
        except: continue

        ds_count = 0 # for surr dataset count
        for surrnum in range(nSur[pscore]):
            # generate surrogate
            try:
                res = pltSSsur(filename, data_dir_path=data_dir, num_comp=num_comp)
            except Exception as e: 
                logger.exception(str(e))
                break
            
            # print(f'[INFO] [{surrnum}] Now at {filename}') # DEBUG

            # construct surrogate file name
            surr_file = filename.split(".")[0]+"_S"+str(surrnum)+"."+filename.split(".")[1]

            # hold the data
            sursdata.append(np.rint(res.T).astype(int))
            sursclass.append(pscore)
            sursfile.append(surr_file)

            ds_count += 1 # count

        print(f'[INFO] {ds_count} surrogate data generated from {filename}')
    

    # v======================= Set work dir ===========================v

    try:
        # delete directory including its content
        # IF wrkdir exist
        shutil.rmtree(r'wrkdir') 
    except:
        shutil.rmtree(r'../wrkdir')
    # create new working directory
    work_dir_path = set_work_dir(r"wrkdir")


    # v=================== Removng Unwanted Class ====================v
    
    if remove_class: # delete class data in 'remove_class' list
        for n_class in remove_class:
            indices = find_elements(np.asarray(sursclass, dtype=object), n_class)
            sursdata = np.delete(sursdata, indices)
            sursclass = np.delete(sursclass, indices)
            sursfile = np.delete(sursfile, indices)
    # TODO: *could be optimized by not generating these surrogate data in the first place


    # v=========================== Saving =============================v
    
    if save_as.lower() == 'pkl':
        print("\nSaving as 'pkl' file")
        save_as_pickle(data=sursdata, score=sursclass, file_name=sursfile, save_to=work_dir_path)

    elif save_as.lower() == 'csv':
        print("\nSaving as 'csv' file")
        save_as_csv(data=sursdata, score=sursclass, file_name=sursfile, save_to=work_dir_path)
    
    print("Save complete!\n")



if __name__ == '__main__':
    # v======================== args parser ===========================v

    import argparse, sys
    
    parser = argparse.ArgumentParser(
        prog = 'Time-series data augmentation',
        description='Generate surrogate time-series data from sample dataset')

    parser.add_argument('-d', '--datadir', dest='data_dir', default='data/ARAT',
                        help='Path to data directory')
    parser.add_argument('-o', '--output', dest='output', default='csv',
                        help='Ouput file (default: csv). Valid options: [csv, pkl]')
    parser.add_argument('-rm', '--remove', dest='remove_ls', default=[], action='append',
                        help='Remove specified class from the output')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--sf', '--scorefile', dest='score_file', required=True,
                        help='File containing score of each sample')
    requiredNamed.add_argument('-f', '--fold', dest='fold', type=int, required=True,
                        help='Number of fold that determine amount of surrogate data generated')
    requiredNamed.add_argument('-n', '--numcomp', dest='num_comp', type=int, required=True,
                        help='Number of components (columns) in a data file')


    # v========================= run project ==========================v

    '<< uncomment the line below and set the apt value if NOT running from terminal (i.e debug mode) >>'
    # sys.argv = ['allSurr1D.py', '-f', '5', '--sf', 'ARscore.txt', '-n', '3', '-o', 'csv']

    args = parser.parse_args()
    data_dir = args.data_dir
    score_file = args.score_file
    save_as = args.output
    fold_no = args.fold
    num_comp = args.num_comp
    remove_ls = args.remove_ls

    # nSur(ratio) depends on the amount of sample in each class (smaller the sample, bigger the nSur value).
    # > to balance the data distribution
    '<< set "nSur=None" to auto set >>'
    # The amount of data generated in each dataset depends on the 
    # "no. of data in the category with highest amount of dataset * fold"
    nSur = None
    '<< or set it manually... >>'
    # e.g
    # nSur = {'0': 12, '1': 6, '2': 1, '3': 1}
    # nSur = {'cannot_perform': 12, 'partially_performed': 6, 'performed_abnormally': 1, 'performs_normally': 1}

    allSurr1D(data_dir=data_dir, score_file=score_file, save_as=save_as, 
                nSur=nSur, fold_no=fold_no, num_comp=num_comp, 
                remove_class=remove_ls)


    '''
    e.g of running on terminal:
    >> python -m allSurr1D -d "data/ARAT" -o pkl --sf 'score.txt' -f 30 -n 3 -rm 0 -rm 2

    # what it does:
    #   - Get data from direcotry "data/ARAT"
    #   - Output as pkl
    #   - Using score file "score.txt"
    #   - Fold the data 30x
    #   - No of columns in each file: 3
    #   - Remove class(score) 0 and 2 from output 
    #     (so e.g if there are 4 classes,[0, 1, 2, 3], only class [1] and [3] will be generated)

    '''