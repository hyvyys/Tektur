#!/bin/bash

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
  fontbakery check-googlefonts -l FAIL ${PARAMS[@]} "../fonts/ttf/*.ttf"

