import os
import natsort

''' Generate score file using defined default value'''
def gen(data_dir='', output_name='score.txt', default='0'):
    # list all files in directory
    files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    # sort in ascending order
    files = natsort.natsorted(files)
    
    output_path = os.path.join(data_dir, output_name)
    # create txt file
    with open(output_path, 'w') as f:
        for i in range(len(files)):
            fn = files[i].partition('.')[0] # file name
            ext = files[i].partition('.')[-1] # file extension

            if ext.lower() == 'csv': 
                f.write(f'{fn} {default}\n')

if __name__ == '__main__':
    gen(data_dir='data/Temperature')