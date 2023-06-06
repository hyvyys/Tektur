#!/bin/bash

fix_masters=1

if [[ $fix_masters == 1 ]]; then
    echo "Fixing FontLab UFO export"
    for master in ./UFO/masters/*.ufo/
    do
      python3 fixMaster.py "${master}"
    done
fi

gftools builder ./UFO/Tektur.designspace
