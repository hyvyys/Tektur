__doc__ = """
    Use on TTF files / directory:
    - shortens nameID 1
    - set glyph class on uni0315 to Simple
    Requires Python 3 and ttx.
"""

import sys
import os
import re
import subprocess

import xml.etree.ElementTree as ET


path = sys.argv[-1]

abbreviations = {
    "Condensed": "Cond",
    # "Narrow": "Nar",
    "Semi": "S",
    "Extra": "X",
    "Light": "Light",
    "Regular": "Reg",
    "Medium": "Med",
    "Bold": "Bold",
    "Black": "Black",
}

def abbreviate(name):
    for key in abbreviations.keys():
        if key in name:
            name = name.replace(key, abbreviations[key])
    # name = name.replace("\\n","")
    # name = name.replace(" ","")
    return(name)


def fixName(ttf):
    subprocess.run(['ttx', '-f', '-t', 'name', ttf])
    ttx = re.sub('.ttf$', '.ttx', ttf)
    tree = ET.parse(ttx)
    nameTable = tree.getroot().find('name')

    def getNameRecord(nameId):
        return next((x for x in nameTable if x.attrib["nameID"] == str(nameId)), None)

    def getName(nameId):
        record = getNameRecord(nameId)
        if record != None:
            return record.text.strip()
        return ""

    family = getName(1)
    style = getName(2)
    family = abbreviate(family)
    comb = family + ' ' + style
    l = len(comb)
    if l > 27:
        print("FAIL  [ " + comb + " ] is " + str(l) + " characters long and exceeds 27 characters")

    getNameRecord(1).text = family
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
    fixName(ttf)
    fixGDEF(ttf)


# check if path is file
if os.path.isfile(path):
    ttxAndFix(path)

if os.path.isdir(path):
    print("is dir")
    for file in os.listdir(path):
        ttxAndFix(path + "/" + file)