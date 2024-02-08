#!/usr/bin/bash -i

# get directories
while getopts b:d: flag
do
    case "${flag}" in
        b) bidsdir=${OPTARG};;
        d) didir=${OPTARG};;
    esac
done

# output
echo "Your BIDS directory is $bidsdir";
echo "Your DICOM directory is $didir";

# make heuristic file
docker --rm --it \
-v $didir:/data:ro \
-v $bidsdir:output \
nipy/heudiconv:latest \
-d /data/{subject}/{session}/*.MRDC.* \
-s sub-005 \
-ss Ser1
-f convertall \
-c none \ 
-o /output
