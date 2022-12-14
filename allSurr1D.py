import os
import re
import shutil
from analyse.routines import *
from pltSSsur import pltSSsur
import logging
from numpy import rint

def allSurr1D(*, data_dir, score_file, save_as, nSur=None, fold_no, num_comp):
    ''' Generate surrogate data for all files in data set

    Input:  
            data_dir - data directory
          score_file - score file containing which class the data belong to
             save_as - output file format (csv/pkl)
                nSur - proportion of surrogate data to be generated (to balance data distribution)
             fold_no - how many times the data is going to augmented (x fold)
             numComp - number of components (columns) in a data file
    
    Returns:
        None (data is stored in wrkdir)
    '''


    # ======================== Initialize ============================

    logger=logging.getLogger() # log

    valid = {'csv', 'pkl'}
    if save_as.lower() not in valid:
        raise ValueError(f"Invalid value for argument 'save_as'! Valid value: {valid}")
    else:
        sursdata = [] # to store generated surrogate data (2D matrix)
        sursclass = [] # to store which class (score) of the data belong to
        sursfile = [] # to store file names (if save as csv and for sanity checking)
    
    try:
        # delete directory including its content
        # IF wrkdir exist
        shutil.rmtree(r'wrkdir') 
    except: 
        pass
    # create new working directory
    work_dir_path = set_work_dir(r"wrkdir")

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
        

    # ======================== Generating ============================

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
            sursdata.append(rint(res.T).astype(int))
            sursclass.append(pscore)
            sursfile.append(surr_file)

            ds_count += 1 # count

        print(f'[INFO] {ds_count} surrogate data generated from {filename}')
    

    # ========================== Saving ==============================
    
    if save_as.lower() == 'pkl':
        print("\nSaving as 'pkl' file")
        save_as_pickle(data=sursdata, score=sursclass, file_name=sursfile, save_to=work_dir_path)

    elif save_as.lower() == 'csv':
        print("\nSaving as 'csv' file")
        save_as_csv(data=sursdata, score=sursclass, file_name=sursfile, save_to=work_dir_path)
    
    print("Save complete!\n")



if __name__ == '__main__':

    ################################## args parser #####################################
    import argparse, sys
    
    parser = argparse.ArgumentParser(
        prog = 'Time-series data augmentation',
        description='Generate surrogate time-series data from sample dataset')

    parser.add_argument('-d', '--datadir', dest='data_dir', default='data',
                        help='Path to data directory')
    parser.add_argument('-s', '--saveas', dest='save_as', default='csv',
                        help='Ouput file (default: csv). Valid options: [csv, pkl]')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('--sf', '--scorefile', dest='score_file', required=True,
                        help='File containing score of each sample')
    requiredNamed.add_argument('-f', '--fold', dest='fold', type=int, required=True,
                        help='Number of fold that determine amount of surrogate data generated')
    requiredNamed.add_argument('-n', '--numcomp', dest='num_comp', type=int, required=True,
                        help='Number of components (columns) in a data file')

    ####################################################################################

    '<< uncomment the line below and set the apt value if NOT running from terminal >>'
    # sys.argv = ['allSurr1D.py', '-f', '30', '--sf', 'score.txt', '-n', '3']

    args = parser.parse_args()
    data_dir = args.data_dir
    score_file = args.score_file
    save_as = args.save_as
    fold_no = args.fold
    num_comp = args.num_comp

    # nSur(ratio) depends on the amount of sample in each class (smaller the sample, bigger the nSur value).
    # > to balance the data distribution
    '<< set "nSur=None" to auto set >>'
    nSur = None
    '<< or set it manually... >>'
    # e.g
    # nSur = {'0': 12, '1': 6, '2': 1, '3': 1}
    # nSur = {'cannot_perform': 12, 'partially_performed': 6, 'performed_abnormally': 1, 'performs_normally': 1}

    allSurr1D(data_dir=data_dir, score_file=score_file, save_as=save_as, nSur=nSur, fold_no=fold_no, num_comp=num_comp)
