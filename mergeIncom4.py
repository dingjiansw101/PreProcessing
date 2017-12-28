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
import re

def poly2origpoly(poly, x, y):
    origpoly = []
    for i in range(int(len(poly)/2)):
        tmp_x = poly[i * 2] + x
        tmp_y = poly[i * 2 + 1] + y
        origpoly.append(tmp_x)
        origpoly.append(tmp_y)
    return origpoly



def main():
    srcpath = r'E:\bod-dataset\results\bod_rfcn_303888'
    dstpath = r'E:\bod-dataset\results\bod_rfcn_303888_nms'
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        name = util.mybasename(fullname)
        #print('name:', name)
        dstname = os.path.join(dstpath, name + '.txt')
        with open(fullname, 'r') as f_in:
            with open(dstname, 'w') as f_out:
                lines = f_in.readlines()
                splitlines = [x.strip().split(' ') for x in lines]
                for splitline in splitlines:
                    subname = splitline[0]
                    #print('subname: ', subname)
                    splitname = subname.split('__')
                    #print('splitname: ', splitname)
                    oriname = splitname[0]

                    pattern1 = re.compile(r'__\d+___\d+')

                    x_y = re.findall(pattern1, subname)
                    #print('x_y: ', x_y)
                    x_y_2 = re.findall(r'\d+', x_y[0])
                    x, y = int(x_y_2[0]), int(x_y_2[1])
                    #print('x:', x)
                    #print('y:', y)
                    confidence = splitline[1]
                    poly = list(map(float, splitline[2:]))
                    origpoly = poly2origpoly(poly, x, y)
                    outline = oriname + ' ' + str(confidence) + ' ' + ' '.join(list(map(str, origpoly)))
                    f_out.write(outline + '\n')
if __name__ == '__main__':
    main()