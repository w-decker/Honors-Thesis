#!/bin/bash

# get flags
while getopts ":b:w:" flag; do
    case "${flag}" in
        b) bids_dir=${OPTARG} ;;
	w) work_dir_parent=${OPTARG};;
        *) echo "Invalid option"; exit 1 ;;
    esac
done

# get subjects
subs=(${bids_dir}/sub-SL*)

for sub in "${subs[@]}"; do
	singularity run --cleanenv -B /data/jdecke5:/data/jdecke5 $HOME/images/fmriprep.simg \
		--work-dir $work_dir_parent/workdir \
		--participant_label "${sub##*/sub-}" \
		--output-spaces T1w \
		--level full \
		--skip-bids-validation \
		--fs-license-file $FREESURFER_HOME/license.txt \
		--cifti-output 91k \
		$bids_dir \
		$bids_dir/derivatives \
		participant
done