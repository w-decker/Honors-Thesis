#!/usr/bin/bash

# get flags
while getopts "b:d:s:" flag; do
    case "${flag}" in
        b) bids_path=${OPTARG} ;;
        d) dcm_path=${OPTARG} ;;
        s) subj=${OPTARG} ;;
        *) echo "Invalid option"; exit 1 ;;
    esac
done

# generate heuristic.py
heudiconv \
-s "$subj" \
-d "$dcm_path/{subject}/*/*.MRDC.*" \
-o "$bids_path" \
-f convertall \
-c none \
--overwrite

# move heuristic files to main dicom dir
cp -r "$bids_path.heudiconv/$subj/info/" "$dcm_path"



