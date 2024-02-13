#!/bin/bash

while getopts "d:s:" flag; do
    case "${flag}" in 
        d) data_dir=${OPTARG} ;;
        s) sub=${OPTARG} ;;
    esac
done

fmriprep-docker \
--work-dir $data_dir/workdir \
--participant_label $sub \
--output-spaces T1w \
--fs-license-file $HOME/fsl/LICENSE.txt \
--cifti-output 91k \
$data_dir \
$dataset_dir/derivatives \
participant

