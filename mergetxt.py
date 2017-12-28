import os
import codecs
import numpy as np
import math
from GetFileFromDir import GetFileFromThisRootDir
import argparse
import cv2
import sympy.geometry as geo
import shapely.geometry as shgeo
import utils as util

subsize = 1024
gap = 80

def poly2origpoly(poly, y, x):
    origpoly = []
    for point in poly:
        tmp_x = point[0] + (subsize - gap) * x
        tmp_y = point[1] + (subsize - gap) * y
        origpoly.append(tmp_x)
        origpoly.append(tmp_y)
    return origpoly


def main():
    filehandles = {}
    srcpath = r'E:\bod-dataset\patches\subcategorylabel\results\patchlabelTxt'
    mergepath = r'E:\bod-dataset\patches\subcategorylabel\results\mergelabelTxt'
    filelist = GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        name = util.mybasename(fullname)
        splitname = name.split('-')[-1]
        initialname = name[0:-(len(splitname) + 1)]
        y = int(splitname.split('_')[0])
        x = int(splitname.split('_')[1])
        objects = util.parse_bod_poly(fullname)
        if initialname not in filehandles:
            outdir = os.path.join(mergepath, initialname + '.txt')
            filehandles[initialname] = codecs.open(outdir, 'w', 'utf_16')
        for obj in objects:
            poly = obj['poly']
            origpoly = poly2origpoly(poly, y, x)
            outline = ' '.join(map(str, origpoly))
            outline = outline + ' ' + obj['name'] + ' ' + str(obj['difficult'])
            ## obj is difficult is the position of difficult is 1, is easy if 0 or empty
            filehandles[initialname].write(outline + '\n')
if __name__ == '__main__':
    main()