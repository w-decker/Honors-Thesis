#!/bin/bash

# get flags
while getopts "b:d:h:" flag; do
    case "${flag}" in
        b) bids_path=${OPTARG} ;;
        d) dcm_path=${OPTARG} ;;
        h) hpy=${OPTARG} ;;
        *) echo "Invalid option"; exit 1 ;;
    esac
done

# remove .heudiconv from bids path to avoid error
# rm -r "$bids_path/.heudiconv"

# get subjects
subs=(${dcm_path}/SL*)

# loop through all subjects
for sub in "${subs[@]}"; do
    # execute conversion
    heudiconv -s "${sub##*/}" \
    -d $dcm_path/{subject}/*/*.MRDC.* \
    -o "$bids_path" \
    -f "$hpy" \
    -c dcm2niix -b \
    --overwrite

    # change file permissions for fMRIPrep
    find $bidspath/sub-${sub##*/} -exec chmod ug+w {} \;
    find $bids_path/.heudiconv/${sub##*/} -exec chmod ug+w {} \;
done