__doc__ = """
    Use on FontLab-produced UFO masters:
    - adds vendor ID to UFO fontinfo
    - adds flattenComponents filter to UFO lib
"""

import sys
from plistlib import load, dump

path = sys.argv[-1]

def fixFontinfo(path):
    with open(path, 'rb') as fp:
        pl = load(fp)
    pl['openTypeOS2VendorID'] = 'Adam'
    
    with open(path, 'wb') as fp:
        dump(pl, fp)

def fixLib(path):
    with open(path, 'rb') as fp:
        pl = load(fp)
    pl['com.github.googlei18n.ufo2ft.filters'] = [{ 'name': 'flattenComponents', 'pre': 1 }]

    with open(path, 'wb') as fp:
        dump(pl, fp)

fixFontinfo(path + 'fontinfo.plist')
fixLib(path + 'lib.plist')
