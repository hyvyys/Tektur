__doc__ = """
    Use on TTF files / directory:
    - set glyph class on uni0315 to Simple
    Requires Python 3 and ttx.
"""

import sys
import os
import re
import subprocess
import xml.etree.ElementTree as ET

path = sys.argv[-1]

def fixFvar(ttf):
    subprocess.run(['ttx', '-f', '-t', 'fvar', ttf])
    ttx = re.sub('.ttf$', '.ttx', ttf)
    tree = ET.parse(ttx)
    fvarTable = tree.getroot().find('fvar')

    def getCoord(namedInstance, axis):
        return next((x for x in namedInstance if x.attrib["axis"] == axis), None)

    for instance in [ instance for instance in fvarTable if instance.tag == "NamedInstance"]:
        wdth = getCoord(instance, 'wdth')
        wdthValue = wdth.attrib["value"]
        if float(wdthValue) != 100.0:
            fvarTable.remove(instance)

    tree.write(ttx, encoding = "UTF-8", xml_declaration = True)
    subprocess.run(['ttx', '-f', '-m', ttf, ttx])
    subprocess.run(['rm', ttx])


def fixGDEF(ttf):
    subprocess.run(['ttx', '-f', '-t', 'GDEF', ttf])
    ttx = re.sub('.ttf$', '.ttx', ttf)
    tree = ET.parse(ttx)
    GlyphClassDef = tree.getroot().find('GDEF').find('GlyphClassDef')

    def getClassDef(glyphName):
        return next((x for x in GlyphClassDef if x.attrib["glyph"] == glyphName), None)

    g = getClassDef('uni0315')
    if g != None:
        g.set('class', '1') # vertical caron is spacing, set to Simple

    tree.write(ttx, encoding = "UTF-8", xml_declaration = True)
    subprocess.run(['ttx', '-f', '-m', ttf, ttx])
    subprocess.run(['rm', ttx])

def ttxAndFix(ttf):
    fixGDEF(ttf)
    fixFvar(ttf)


# check if path is file
if os.path.isfile(path):
    ttxAndFix(path)

if os.path.isdir(path):
    print("is dir")
    for file in os.listdir(path):
        ttxAndFix(path + "/" + file)