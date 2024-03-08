#!/bin/bash

# locations
ds_path=</path/to/dataset/>
bids_path=</path/to/bids/output/>
hpy=</path/to/heuristic.py/>

# activate conda env
conda activate bids # see `setup.sh` to create bids env

PATH=$PATH:~/.local/bin

# remove .heudiconv from bids path to avoid error
rm -r "$bids_path/.heudiconv"

# get subjects
subs=(SL*) # glob based on naming convention

# loop throguh all subjects
for sub in $subs
do
    heudiconv -s $sub \
    -d $dcm_path/{subject}/*/*.MRDC.* \
    -o $bids_path\
    -f $hpy \
    -c dcm2niix -b \
    --overwrite
done

# change file permissions for fMRIPrep
find $bidspath/sub-${$subs//_} -exec chmod ug+w {} \;
find $bids_path/.heudiconv/${pid//_} -exec chmod ug+w {} \;