import os

def split(filehandler, delimiter=',', row_limit=106, 
    output_name_template='temperature_%s.csv', output_path='data/Temperature', keep_headers=False):
    """
    Splits a CSV file into multiple pieces.
    
    Arguments:
        row_limit: The number of rows you want in each output file. 10,000 by default.
        output_name_template: A %s-style template for the numbered output files.
        output_path: Where to stick the output files.
        keep_headers: Whether or not to print the headers in each output file.
    
    Example usage:
        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('data/big_dataset.csv', 'r'));
    
    """
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
         output_path,
         output_name_template  % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w', newline=''), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
               output_path,
               output_name_template  % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w', newline=''), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

if __name__ == '__main__':
    split(open('old/dataset_co2.csv', 'r'))