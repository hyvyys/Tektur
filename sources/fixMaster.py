__doc__ = """
    Use on FontLab-produced UFO masters:
    - adds vendor ID
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

fixFontinfo(path)