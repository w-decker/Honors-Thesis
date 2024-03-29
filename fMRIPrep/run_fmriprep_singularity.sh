#!/bin/bash

# get flags
while getopts ":b:w:f:" flag; do
    case "${flag}" in
        b) bids_dir=${OPTARG};;
        w) work_dir_parent=${OPTARG};;
        f) fs_license=${OPTARG};;
        *) echo "Invalid option"; exit 1 ;;
    esac
done

# get subjects
subs=(${bids_dir}/sub-SL*)

for sub in "${subs[@]}"; do
    singularity run --cleanenv -B /data/jdecke5:/data/jdecke5 $HOME/images/fmriprep.simg \
        $bids_dir $bids_dir/derivatives participant \
        --work-dir $work_dir_parent \
        --participant_label "${sub##*/sub-}" \
        --output-spaces T1w \
        --level full \
        --skip-bids-validation \
        --fs-license-file "${fs_license}" \
        --cifti-output 91k

done