#!/bin/bash

# echo "Fixing FontLab UFO export"
for master in ./UFO/masters/*.ufo/
do
  python3 fixMaster.py "${master}"
done

gftools builder ./config.yaml

# echo "Post-processing static TTF fonts"
for ttf in $(ls ../fonts/ttf/*.ttf)
do
    python3 fixStatic.py $ttf
done
