#!/usr/bin env python

# imports for this module
import pandas as pd
import numpy as np
import os 
from scipy.stats import ttest_1samp

class FindFiles:
    """Class for getting all the files you wish to analyze and putting them in a single object
    
    Parameters
    ----------
    path: str, default: current path
        Absolute path to the folder which holds data files.
        Must be in .csv format
    """

    def __init__(self, path=os.path.dirname(os.path.abspath(__name__))):
        self.path = path
        self.files = os.listdir(self.path)

    def parse_file(self, subids):
        """Find all of the files you wish to score
        
        Parameters
        ----------
        subids: list
            List of subject IDs that match the filenames. 
            Example: subids = ['sub-001', 'sub-002', 'sub-003']
        """
        
        files = []
        for id in subids:
            found= False
            for filename in self.files:
                filename2 = filename.split('_')[0]
                if id == filename2 and filename.endswith('.csv'):
                    files.append(os.path.join(self.path, filename))
                    found = True
                    break
                if not found:
                    print('Getting more files')
        
        # return
        self.files = files

def clean_3afc(d):
    """Remove erroneous columns from .csv file generated from PsychoPy

    Parameters
    ----------
    d: str 
        absolute path to csv file generated from 3afc post-test
    """
    # read in the datafile
    df = pd.read_csv(d)

    # determine which order
    order = []
    if df['blocks'][5] == 'block1.csv':
        order = 1
    elif df['blocks'][5] == 'block12.csv':
        order =2

    # get subject ID
    fn = d.split('/')[-1] # filename
    subid = fn.split('_')[0] #subject ID

    # remove unnecessary columns 
    label = ['example_outer_loop.thisRepN',
    'example_outer_loop.thisTrialN',
    'example_outer_loop.thisN',
    'example_outer_loop.thisIndex',
    'example_inner_loop.thisRepN',
    'example_inner_loop.thisTrialN',
    'example_inner_loop.thisN',
    'example_inner_loop.thisIndex',
    'example_shift_loop.thisRepN',
    'example_shift_loop.thisTrialN',
    'example_shift_loop.thisN',
    'example_shift_loop.thisIndex',
    'trials_loop.thisRepN',
    'trials_loop.thisTrialN',
    'trials_loop.thisN',
    'trials_loop.thisIndex',
    'transition_loop.thisRepN',
    'transition_loop.thisTrialN',
    'transition_loop.thisN',
    'transition_loop.thisIndex',
    'blocks_loop.thisRepN',
    'blocks_loop.thisTrialN',
    'blocks_loop.thisN',
    'blocks_loop.thisIndex',
    'word_loop.thisRepN',
    'word_loop.thisTrialN',
    'word_loop.thisN',
    'word_loop.thisIndex',
    'replay_msg_loop.thisRepN',
    'replay_msg_loop.thisTrialN',
    'replay_msg_loop.thisN',
    'replay_msg_loop.thisIndex',
    'instructions1_key.keys',
    'instructions1_key.rt',
    'instructions2_key.keys',
    'instructions2_key.rt',
    'instructions3_key.keys',
    'instructions3_key.rt',
    'instructions4_key.keys',
    'instructions4_key.rt',
    'shift1.started',
    'shift1.stopped',
    'shift2_2.started',
    'shift2_2.stopped',
    'instructions5_key.keys',
    'instructions5_key.rt',
    'word_sound.started',
    'word1_shape.started',
    'word_sound.stopped',
    'word1_shape.stopped',
    'jitter_shape.started',
    'jitter_shape.stopped',
    # 'shift2_shape.started',
    # 'shift2_shape.stopped',
    'replay_msg_text.started',
    'response_text.started',
    'key_resp.started',
    'replay_msg_text.stopped',
    'participant',
    'order',
    'date',
    'expName',
    'psychopyVersion',
    'frameRate']

    df = df.drop(columns=label)

    return order, df, subid

def create_anskey(order):
    """Create answer key data frame

    Parameters
    ----------
    order: int
        1 or 2. This is also calculated and returned in clean_3afc() 
    """

    # assign in order
    order = order

    # create empty df for scoring
    anskey = pd.DataFrame(columns=['correct_key_resp', 'actual_key_resp', 'assign_codes', 'score'])

    # set answer key based on order set a few chunks earlier
    answers =  ['z', 'v', 'v',  'z', 'm', 'z', 'z','v', 'm','v', 'v', 'm']
    if order == 1:
        anskey['correct_key_resp'] = answers
    elif order == 2:
        anskey['correct_key_resp'] = answers[::-1]

    return anskey

def merge_participant_data(df, anskey):
    """Combine scores from individual participants to the answer key

    Parameters
    ----------
    df: pandas.DataFrame()
        The RETURNED data frame generated in clean_3afc()

    anskey: pandas.DataFrame()
        The RETURNED data frame generated in create_anskey()
    """
    anskey['actual_key_resp'] = list(df['key_resp.keys'][5:29].dropna())

    return anskey

def score(anskey):
    """Scoring individual participant data

    Parameters
    ----------
    anskey: pandas.DataFrame()
        The RETURNED data frame generated in merge_participant_data()
    """

    # assign codes
    for i in range(12):
        if anskey['correct_key_resp'][i] == anskey['actual_key_resp'][i]:
            anskey['assign_codes'][i] = 1
        else:
            anskey['assign_codes'][i] = 0

    # get score
    anskey['score'] = (sum(anskey['assign_codes']))/12;

    # output
    score= anskey['score'][1];
    
    return anskey, score

def manage_scores(score, participant_database, subid):
    """
    Integrate scores with participant database for future statistical analysis.
    There must be a subject ID column and a scores column.

    NOTE: You must have "openpyxl" installed.

    Parameters
    ----------
    score: int
        Integer score generated from score()
    
    participant_database: str
        absolute path to .xslx file

    subid: str
        Subject ID RETURNED in clean_3afc() OR custom subject ID. 
        MUST match with subject ID in participant database.
    """

    # get participant database
    pdb = pd.read_excel(participant_database)

    # set subject id
    subid = subid

    # find subject id index
    idx = pdb[pdb['sub_id'] == subid].index[0]

    # assign score to participant database in correct column and row
    pdb['score'][idx] = score

    pdb_scores = pdb['score']

    return pdb_scores

def score_stats(scores, mu=(1/3)):
    """Compute a 1 sample, 1 tailed t-test
    
    Parameters
    ----------
    pdb_scores: pandas.DataFrame()
        Data frame of participant scores RETURNED by manage_scores()

    mu: int, default: (1/3)
        Population mean that you are testing against

    """
    
    # get scores
    scores = scores

    # compute test
    m = ttest_1samp(scores, popmean=mu, alternative='greater')

    return m

