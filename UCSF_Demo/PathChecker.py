import os

def check_path(path):
    
    '''
    This function creates a directory for the provided path if the path does not point to a directory that exists
    '''

    if not os.path.exists(path):
        
        os.makedirs(path)
