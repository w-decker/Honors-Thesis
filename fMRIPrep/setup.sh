#!/bin/bash

conda create -n fmriprep
conda activate fmriprep
python3.11 -m pip install fmriprep-docker
conda install pip
~/opt/anaconda3/envs/fmriprep/bin/pip install fmriprep-docker
conda env export > environment.yml