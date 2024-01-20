#!/usr/bin/bash -i

while getopts d: flag
do
    case ${flag} in 
        d) path=${OPTARG};;
    esac
done

tar -kxvzf ${path} -C ${path}