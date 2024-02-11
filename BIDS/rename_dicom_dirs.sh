#!/bin/bash

# get directory
while getopts d: flag
do
    case "${flag}" in
        d) directory=${OPTARG};;
    esac
done

# rename based on prespecified nameing scheme
for folder in "$directory"/*; do
    if [ -d "$folder" ]; then
        case "$(basename "$folder")" in
            Ser1)
                new_name="anat_local"
                ;;
            Ser3)
                new_name="t1w"
                ;;
            Ser4)
                new_name="dti"
                ;;
            Ser5)
                new_name="resting_state"
                ;;
            Ser6)
                new_name="stat_learning"
                ;;
            Ser400)
                new_name="avg_dc"
                ;;
            Ser401)
                new_name="fractional_aniso"
                ;;
            Ser402)
                new_name="isotrop"
                ;;
            *)
                echo "No renaming for folder $(basename "$folder")"
                continue
                ;;
        esac

        # Rename the folder
        mv "$folder" "$directory/$new_name"
        echo "Renamed $(basename "$folder") to $new_name"
    fi
done
