import os
import re
import shutil
from analyse.routines import *
from pltSSsur import pltSSsur
import logging

def allSurr1D(*, data_dir, score_file, save_as, nSur=None, fold_no, numComp):
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
    if save_as not in valid:
        raise ValueError(f"Invalid value for argument 'save_as'! Valid value: {valid}")
    
    try:
        # delete directory including its content
        shutil.rmtree(r'wrkdir') 
    except: 
        pass
    # set working directory
    work_dir_path = set_work_dir(r"wrkdir")

    # get the score from txt file
    data_score = dict()
    with open(os.path.join(data_dir,score_file)) as score:
        for line in score.readlines():
            data_score[line.split()[0]] = line.split()[1]
    
    # manually set nSur
    if nSur != None:
        # multiple each value to the number of fold
        nSur = {key: value * fold_no for key, value in nSur.items()}

    # auto nSur
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

        # get the 
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

        ds_indx = 0 # surr dataset count
        for surrnum in range(nSur[pscore]):
            # generate surrogate
            try:
                res = pltSSsur(filename, data_dir_path=data_dir, numComp=numComp)
            except Exception as e: 
                logger.exception(str(e))
                break

            # save syntensized data
            # print(f'[INFO] [{surrnum}] Now at {filename}')
            if save_as == 'csv':
                # construct surrogate file name
                surr_file = filename.split(".")[0]+"_S"+str(surrnum)+"."+filename.split(".")[1]
                file_path = os.path.join(work_dir_path, str(pscore), surr_file)
                save_as_csv(res.T, file_path)
            elif save_as == 'pkl':
                raise Exception("pkl is not implemented")
                save_as_pickle() #TODO
            ds_indx += 1

        print(f'[INFO] {ds_indx} surrogate data generated from {filename}')



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

    '<< uncomment the line below and set apt value if NOT running from terminal >>'
    # sys.argv = ['allSurr1D.py', '-f', '30', '--sf', 'score.txt', '-n', '3']

    args = parser.parse_args()
    data_dir = args.data_dir
    score_file = args.score_file
    save_as = args.save_as
    fold_no = args.fold
    num_comp = args.num_comp

    # nSur(ratio) depends on the amount of sample in each class (smaller the sample, bigger the nSur value).
    # to balance the data distribution
    '<< set "nSur=None" to auto set >>'
    nSur = None
    '<< or set it manually... >>'
    # e.g
    # nSur = {'0': 12, '1': 6, '2': 1, '3': 1}
    # nSur = {'cannot_perform': 12, 'partially_performed': 6, 'performed_abnormally': 1, 'performs_normally': 1}

    allSurr1D(data_dir=data_dir, score_file=score_file, save_as=save_as, nSur=nSur, fold_no=fold_no, numComp=num_comp)
