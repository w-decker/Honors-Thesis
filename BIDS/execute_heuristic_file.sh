#!/bin/bash
#
#SBATCH --job-name=bids
#SBATCH --output=array-out/bids-%A-%a.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=express
#SBATCH --time=30:00
#SBATCH --mem-per-cpu=8G
#SBATCH --mail-type=FAIL

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
subs=(SL*)
pid="${subs[$SLURM_ARRAY_TASK_ID]}"

# execute conversion
heudiconv -s $pid \
-d $dcm_path/{subject}/*/*.MRDC.* \
-o $bids_path\
-f $hpy \
-c dcm2niix -b \
--overwrite

# change file permissions for fMRIPrep
find $bidspath/sub-${pid//_} -exec chmod ug+w {} \;
find $bids_path/.heudiconv/${pid//_} -exec chmod ug+w {} \;



