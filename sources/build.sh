#!/bin/bash

fix_masters=1
export_variable=1
export_static=1
# fontbakery=1


if [[ $fix_masters == 1 ]]; then
    echo "Fixing FontLab UFO export"
    for master in ./UFO/masters/*.ufo/
    do
      python3 fixMaster.py "${master}"
    done
fi


variableFont="../fonts/variable/Tektur[wdth,wght].ttf"

if [[ $export_variable == 1 ]]; then
    echo "Building variable TTF font"
    designspace="Tektur-variable"
    source="../fonts/variable/${designspace}-VF.ttf"
    target=$variableFont
    backup="../fonts/variable/${designspace}-VF-backup-fonttools-prep-gasp.ttf";

    fontmake --verbose WARNING --flatten-components -m "./UFO/${designspace}.designspace" -o variable --output-dir ../fonts/variable

    echo "Post-processing variable TTF font"
    python3 fixVariable.py $source
    gftools fix-nonhinting $source $target
    gftools fix-dsig -f $target;
    rm $source
    rm $backup
fi


if [[ $export_static == 1 ]]; then
    echo "Building static TTF fonts"
    rm -R ./UFO/instances/
    fontmake --verbose WARNING --flatten-components -m ./UFO/Tektur-static.designspace -o ttf --output-dir ../fonts/ttf -i

    echo "Post-processing static TTF fonts"
    for ttf in $(ls ../fonts/ttf/*.ttf)
    do
        python3 fixStatic.py $ttf
        python3 -m ttfautohint $ttf $ttf
        gftools-fix-hinting.py $ttf
        mv "$ttf.fix" $ttf
        gftools-fix-dsig.py -f $ttf
    done
fi


if [[ $fontbakery == 1 ]]; then
  echo "Running checks"

  PARAMS=(
    -x "com.google.fonts/check/family/tnum_horizontal_metrics" # https://github.com/googlefonts/fontbakery/issues/2278#issuecomment-739417643
    -x "com.google.fonts/check/name/match_familyname_fullfont" # https://github.com/googlefonts/fontbakery/issues/2254
    -x "com.google.fonts/check/name/familyname"
      # fails with shortened family names
      # which are required to pass com.google.fonts/check/name/family_and_style_max_length
      # can't have cookie and eat cookie, so bye-bye!
    -x "com.google.fonts/check/contour_count"                  # percent and others have specific design
    -x "com.google.fonts/check/outline_short_segments"         # W has narrow inktraps
    -x "com.google.fonts/check/outline_jaggy_segments"         # W has narrow inktraps
    -x "com.google.fonts/check/outline_colinear_vectors"       # I has concave serifs; not really colinear, this check is wrong
    -x "com.google.fonts/check/outline_alignment_miss"         # fails because of accents like tilde
    -x "com.google.fonts/check/gdef_mark_chars"                # uni0315 in this font is spacing and contains no anchors
  )
  fontbakery check-googlefonts --succinct -l WARN $variableFont
  fontbakery check-googlefonts --succinct -l WARN ${PARAMS[@]} ../fonts/ttf/

fi
