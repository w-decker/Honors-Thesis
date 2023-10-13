#!/usr/bin/env python

# imports for this module
import pandas as pd
import os 
from scipy.stats import ttest_1samp, ttest_ind

class Data(object):
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

    def parse_files(self, subids):
        """Find all of the files you wish to score
        
        Parameters
        ----------
        subids: list, str
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
                    print('Looking for more files')
        
        # return
        self.files = files
        self.numfiles = len(files)

    def rm_subs(self, subids):
        """Remove subjects' files from object

        Parameters
        ----------
        subids: list
             List of subject IDs that match the filenames. 
        """

        # bring in current files
        files = self.files

        # get sub ids
        subids = subids

        # remove requested files
        _2rm = []
        for file in files:
            for id in subids:
                if file.split('/')[-1].split('_')[0] == id:
                    _2rm.append(file)

        [files.remove(i) for i in _2rm]

        # return new
        self.files = files
        self.numfiles = len(files)


    def clean_3afc(self):
        """Remove erroneous columns from .csv file generated from PsychoPy"""

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

        # read in the datafile
        for i in self.files:
            df = pd.read_csv(i)
            try:
                df = df.drop(columns=label)
                df.to_csv(i)
            except:
                KeyError

        return self

    def score(self):
        """Scoring individual participant data"""

        # create empty df for scoring
        anskey = pd.DataFrame(columns=['correct_key_resp', 'actual_key_resp', 'assign_codes', 'score'])

        str_scores = []
        rand_scores = []

        for i in self.files:

            # read in the file
            df = pd.read_csv(i)

            order = []
            if df['blocks'][5] == 'block1.csv':
                order = 1
            elif df['blocks'][5] == 'block12.csv':
                order = 2

            anskey['actual_key_resp'] = list(df['key_resp.keys'][5:29].dropna())

            # set answer key based on order set a few chunks earlier
            answers =  ['z', 'v', 'v',  'z', 'm', 'z', 'z','v', 'm','v', 'v', 'm']
            if order == 1:
                anskey['correct_key_resp'] = answers
            elif order == 2:
                anskey['correct_key_resp'] = answers[::-1]

            for j in range(12):
                if anskey['correct_key_resp'][j] == anskey['actual_key_resp'][j]:
                    anskey['assign_codes'][j] = 1
                else:
                    anskey['assign_codes'][j] = 0
            # get score
            anskey['score'][0] = (sum(anskey['assign_codes']))/12;
            score = anskey['score'][0]
        
            fn = i.split('/')[-1] # filename
            cond = fn.split('_')[1].split('.')[0] #condition

            if cond == 'structured':
                str_scores.append(score)
            elif cond == 'random':
                rand_scores.append(score)

        scores = pd.DataFrame(columns=['structured', 'random'])
        try:
            scores['structured'] = str_scores
            scores['random'] = rand_scores
        except:
            ValueError

        self.anskey = anskey
        self.scores = scores

        return self


class Stats(Data):
    """Class to compute a 1 sample, 1 tailed t-test or two-samples independant, two tailed t-test
    

    """
    def __init__(self, scores):
        super().__init__() # gets 'self' from previous class

        self.scores=scores

    def compute(self, test, **kwargs):
        '''Method for calculating scores
        
        Parameters
        ----------
        test: str or int
            Choose which statistical test you want to computer. 
            1 or '1samp' = 1 sample, 1 tailed t-test
            2 or 'ind' = two samples, independet, two-tailed t-test

        Keyword Arguments
        -----------------
        mu: int
            Population parameter you wish to test agains. Only necessary if test = 1samp
        '''
                
        if test == 1 or test.lower() == '1samp':
            self.test = '1samp'
        elif test == 2 or test.lower()=='ind':
            self.test = 'ind'

        self.mu = kwargs.get('mu')
        if self.mu is None and self.test == '1samp':
            raise KeyError('When conducting a 1 sample t-test, you must provide the population parameter (mu). \n +\
                           In the case of this project, mu= (1/3)')

        if self.test == '1samp':
             # compute test
            statistic = ttest_1samp(self.scores['structured'], popmean=self.mu, alternative='greater')

        elif self.test == '1samp':
            # compute test
            statistic = ttest_ind(a=self.scores['structured'], b=self.scores['random'], equal_var=False, alternative='two-sided')

        self.statistic=statistic
        return self
