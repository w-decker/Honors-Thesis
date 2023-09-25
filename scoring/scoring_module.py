#!/usr/bin env python

# imports for this module
import pandas as pd
import numpy as np

# testing [delete later]

d = pd.read_csv('testdata/sub-001-3afc.csv')

# check_dataset()
def check_dataset(task, file):
    '''
    This function checks whether the datafile meets the proper criterion to be analyzed.

    Parameters
    ----------

    task: int (0 | 1)
    type of task to be analyzed. O=3afc, 1=go-no-go

    file: pandas.DataFrame()
    Pandas dataframe of the file to be analyzed
    ''' 

    # parse inputs
    df = file
    if task == 0:
        task = '3afc'
    elif task == 1:
        task = 'go-no-go'

    g = d.split('-')

