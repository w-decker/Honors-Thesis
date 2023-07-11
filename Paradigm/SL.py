import pandas as pd
from psychopy.sound.backend_ptb import SoundPTB
from psychopy import gui
import time

# load stimuli
sounds = pd.read_csv('/Users/lendlab/Box Sync/willdecker/LSU Undergrad/Honors-Thesis/github/Honors-Thesis/Paradigm/structured_orders_predetermined_words.csv')
sounds = sounds['Order 1']
sound_dir = '/Users/lendlab/Desktop/sounds/'

# set conditions
myDlg = gui.Dlg(title='Set Condition and Order')
myDlg.addText('Condition')
myDlg.addField('Condition:', choices=['structured', 'random'])
myDlg.addText('Order')
myDlg.addField('Order:', choices=['1', '2'])
ok_data = myDlg.show()  

# play structured, order 1
if ok_data[0] == 'structured' and ok_data[1] == '1':
    sounds = pd.read_csv('/Users/lendlab/Box Sync/willdecker/LSU Undergrad/Honors-Thesis/github/Honors-Thesis/Paradigm/structured_orders_predetermined_words.csv')
    sounds = sounds['Order 1']
    for i in range(len(sounds)):
        time.sleep(1.0)
        sound_2_play = SoundPTB(value=(sound_dir + sounds[i] + '.wav'), secs=0.50, blockSize=128, preBuffer=-1)
        sound_2_play.play()
        time.sleep(0.50)
        
# play structured, order 2        
elif ok_data[0] == 'structured' and ok_data[1] == '2': 
    sounds = pd.read_csv('/Users/lendlab/Box Sync/willdecker/LSU Undergrad/Honors-Thesis/github/Honors-Thesis/Paradigm/structured_orders_predetermined_words.csv')
    sounds = sounds['Order 2']
    for i in range(len(sounds)):
        time.sleep(1.0)
        sound_2_play = SoundPTB(value=(sound_dir + sounds[i] + '.wav'), secs=0.50, blockSize=128, preBuffer=-1)
        sound_2_play.play()
        time.sleep(0.50)

# play random, order 1
elif ok_data[0] == 'random' and ok_data[1] == '1': 
    sounds = pd.read_csv('/Users/lendlab/Box Sync/willdecker/LSU Undergrad/Honors-Thesis/github/Honors-Thesis/Paradigm/random_orders.csv')
    sounds = sounds['Order 1']
    for i in range(len(sounds)):
        time.sleep(1.0)
        sound_2_play = SoundPTB(value=(sound_dir + sounds[i] + '.wav'), secs=0.50, blockSize=128, preBuffer=-1)
        sound_2_play.play()
        time.sleep(0.50)
        
# play random, order 2
elif ok_data[0] == 'random' and ok_data[1] == '2': 
    sounds = pd.read_csv('/Users/lendlab/Box Sync/willdecker/LSU Undergrad/Honors-Thesis/github/Honors-Thesis/Paradigm/random_orders.csv')
    sounds = sounds['Order 2']
    for i in range(len(sounds)):
        time.sleep(1.0)
        sound_2_play = SoundPTB(value=(sound_dir + sounds[i] + '.wav'), secs=0.50, blockSize=128, preBuffer=-1)
        sound_2_play.play()
        time.sleep(0.50)
        
