__doc__ = """
    Use on TTF files / directory:
    - shortens nameID 1
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
    "SemiCondensed": "SemiCond",
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
    short_family = abbreviate(family)
    ttf_new = abbreviate(ttf)
    
    comb = short_family + ' ' + style
    l = len(comb)
    if l > 27:
        print("FAIL  [ " + comb + " ] is " + str(l) + " characters long and exceeds 27 characters")

    getNameRecord(1).text = short_family
    tree.write(ttx, encoding = "UTF-8", xml_declaration = True)
    subprocess.run(['ttx', '-f', '-m', ttf, ttx])
    subprocess.run(['rm', ttx])
    subprocess.run(['mv', ttf, ttf_new])


def ttxAndFix(ttf):
    fixName(ttf)


# check if path is file
if os.path.isfile(path):
    ttxAndFix(path)

if os.path.isdir(path):
    print("is dir")
    for file in os.listdir(path):
        ttxAndFix(path + "/" + file)