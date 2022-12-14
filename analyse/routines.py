
def set_data_file(file_name, data_dir_path):
    '''set data path

    Syntax: [file_abs_path] = set_data_file(file_name)

    Returns
    -------
        file_abs_path - absolute path to the data file
    '''

    import os

    # os.path.join will concatenate the path.
    # os.path.abspath will interprate os.pardir as 
    # going up by one directory + return abs path.
    file_abs_path = os.path.abspath(os.path.join(data_dir_path, file_name))

    return file_abs_path



def read_BIN(): #TODO
    '''
    read binary data
    '''
    readOk = False


    pass



def get_min(V):
    from numpy import mean, power, argmin
    from math import log

    # estimate RDE per Braun given sorted eigenvalues in V
    V0 = V - mean(V)
    N = len(V)
    nlgd = []

    for d in range(N-1): # length of data
        sig1 = sum(power(V0[0:d+1], 2)) / (d+1)
        sig2 = sum(power(V0[d+1:], 2)) / (N-d-1)
        res = log(sig1 ** 2) * (d+1) / N + log(sig2 ** 2) * (N-d-1) / N
        nlgd.append(res)

    return argmin(nlgd)
    

    
def set_work_dir(dir_name):
    ''' Create working directory

    Syntax: [work_dir_path] = set_work_dir(drv)

    Create directory to store the generated surrogate data,
    clear the directory first if it's not empty.

    Input: dir_name - directory name

    Returns
    -------
    work_dir_path - absolute path to working directory
    
    '''

    import os

    # get current file (routines.py) path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # get relative path to parent dir + join with work dir name
    work_dir_path = os.path.abspath(os.path.join(current_dir, os.pardir, dir_name))

    # create the directory
    try:
        # os.makedirs() method will raise an OSError if the directory
        # to be created already exists. But It can be suppressed by
        # setting the value of a parameter exist_ok as True
        os.makedirs(work_dir_path, exist_ok=True)
        print(f'[INFO] Directory {work_dir_path} is created successfully!')
    except OSError as error:
        print(f'[ERROR] Directory {work_dir_path} can\'t be created')
    
    return work_dir_path



def save_as_csv(*, data:list, score:list, file_name:list, save_to):
    ''' Save result as CSV

    Syntax: set_work_dir(res, filename, index)

    Create directory of classes (according to 'Score'),
    result is saved in respective directory

    Input:      res - result to be stored as csv
           filename - path to where file is stored (inc. file name)

    Returns
    -------
    None
    '''
    import os
    from numpy import savetxt
    from tqdm import tqdm # progress bar

    for i in tqdm(range(len(data))):
        file_path = os.path.join(save_to, str(score[i]), file_name[i])

        file_split = os.path.split(file_path)
        try:
            os.makedirs(file_split[0])
            # print(f'[INFO] Directory {file_split[0]} is created successfully!')
        except OSError as error:
            pass
    
        savetxt(file_path, data[i], delimiter=',') # csv is essentially fancy txt



def save_as_pickle(*, data:list, score:list, file_name:list, save_to):
    import pickle
    import os

    packed_data = {"sursdata": data, "sursclass": score, "sursfile": file_name}
    pkl_file = os.path.join(save_to, "surs.pkl")

    f = open(pkl_file, "wb") # w: write, b:binary
    f.write(pickle.dumps(packed_data))
    f.close()