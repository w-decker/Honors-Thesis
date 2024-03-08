#!/bin/bash

while getopts :p: flag
do
    case ${flag} in 
        p) path=${OPTARG};;
    esac
done

subs=(${path}/*.tgz)

for sub in "${subs[@]}"; do
    tar -xvzf "${sub}" -C "${path}"
done