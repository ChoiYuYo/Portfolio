"""
Package: CompressPNG
Module:  CompressPNG
Purpose: Provides a PNG Compress keyword wrapper for the RobotFramework screenshot
         
"""
__author__  = "Xia Clark <joehisaishi1943@gmail.com>"
__version__ = "0.2"
#
# Import the libraries we need
#
try :
    from PIL import Image
except :
    ImageGrab = None
from os import listdir
from os.path import isfile, join
import os

#
#-------------------------------------------------------------------------------
#
class CompressPNG(object):
    def __init__(self):
        pass

    def isPNG(self, filePath):
        if isfile(filePath):
            if '.PNG' in filePath or '.png' in filePath:
                return True
        else:
            return False

    def compressPNG(self, mypath, colorArea=128):
        onlyfiles = [f for f in listdir(mypath) if self.isPNG(join(mypath, f))]
        print(onlyfiles)
        for pic in onlyfiles:
            print("b4: ", os.stat(pic).st_size)
            im: Image.Image = Image.open(pic)
            im = im.quantize(colors=colorArea)
            im.save(pic, optimize=True)
            print("after: ", os.stat(pic).st_size)
