
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

    Syntax: save_as_csv(data, score, file_name, save_to)

    Save all the data stored in data list as csv.

    Input:     data - list of generated surrogate data (2D Matrix)
              score - list of the scores corresponding to data
          file_name - list of the file names corresponding to data
            save_to - path to where the csv files will be store

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
    ''' Save result as PKL

    Syntax: save_as_pkl(data, score, file_name, save_to)

    Save all the data stored in data list as pkl.

    Input:     data - list of generated surrogate data (2D Matrix)
              score - list of the scores corresponding to data
          file_name - list of the file names corresponding to data
            save_to - path to where the csv files will be store

    Returns
    -------
    None
    '''
    import pickle
    import os

    packed_data = {"sursdata": data, "sursclass": score, "sursfile": file_name}
    pkl_file = os.path.join(save_to, "surs.pkl")

    with open(pkl_file,'wb') as file_handle:
        pickle.dump(packed_data, file_handle, protocol=pickle.HIGHEST_PROTOCOL)


def find_elements(records_array, val):
    ''' Find indices of a given element in np.array

    Syntax: find_elements(records_array, val)

    returns a vector containing the linear indices of given element in records_array.

    Input:    records_array - numpy array
                        val - value to be compared

    Returns
    -------
    all_elemements_index - vector containing all indices of given element in records_array
    '''
    # technically you can use np.where() directly but it's slow if the array is big

    import numpy as np

    # return index of sorted arr (sorted by unique element)
    idx_sort = np.argsort(records_array)
    # sorts records array so all unique elements are together 
    sorted_records_array = records_array[idx_sort]
    # returns the unique values, the index of the first occurrence of a value, and the count for each element
    vals, idx_start, count = np.unique(sorted_records_array, return_counts=True, return_index=True)
    # find the starting index of a given value
    index = np.where(vals==val)[0][0]
    # get the range of the 'grouped' elements
    start = idx_start[index]
    end = idx_start[index+1] if index+1 != len(idx_start) else -1

    # get the original indices of the given element
    all_elements_index = idx_sort[start:end]
    
    return all_elements_index
    