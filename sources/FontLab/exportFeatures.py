#FLM: Export features to DesignSpace-UFO

import os
import fontlab
from typerig.proxy.fl.objects.font import pFont

font = pFont()
prefix = font.getFeaPrefix()
features = '\n'.join(font.getFeatures())
text = prefix + '\n' + features

layerName = font.pGlyphs()[0].activeLayer().name
path = os.path.dirname(font.path) + \
  "/masters/" + "Tektur" + "-" + \
  layerName + ".ufo/features.fea"

f = open(path, "w")
f.write(text)
f.close()

print 'written features to: ' + path