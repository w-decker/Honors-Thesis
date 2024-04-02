import numpy as np
from sklearn.model_selection import KFold, LeaveOneOut
import pandas as pd
from brainiak.eventseg.event import EventSegment
import sys
from decker.analysis.eventseg.eventseg import *
import os

# run 
if __name__ == '__main__':

    # import data
    DATA = np.load(sys.argv[1], allow_pickle=True)[()]

    # ensure data is in correct format
    assert isinstance(DATA, np.ndarray)

    # set output dir
    OUT = sys.argv[2]

    # make sure output dir exists
    if not os.path.exists(OUT):
        raise FileNotFoundError
    
    # get number of splits
    if not sys.argv[3]:
        n_splits = 4
    else:
        n_splits = int(sys.argv[3])
    
    print('Running: Leave-one-out nested cross validation')
    print('----------------------------------------------\n')
    
    # extract some variables
    print(f'Acquiring some data...\n')

    n_subs = DATA.shape[0]
    idx = np.array([i for i in range(n_subs)])
    k_vals = np.arange(3, 15, 1) # this is hardcoded

    # begin
    results = outerLoop(idx=idx, n_splits=n_splits, data=DATA, k_vals=k_vals)

    # save results
    results.to_csv(os.path.join(OUT, sys.argv[4]))

    print('Complete: Leave-one-out nested cross validation')
    print('-----------------------------------------------\n')

    print(f'Results output to {OUT}')