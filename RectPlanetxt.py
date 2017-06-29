#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math
import numpy as np
import argparse
import GetFileFromDir as GetFile

def recto4dot(rect):
    #rect[1-4] ,x, y, w, h
    x, y, w, h = rect[0] - rect[2]/2, rect[1] - rect[3]/2, rect[2], rect[3]

    dots = np.zeros(8, dtype=np.int)
    dots[0] = x#x1
    dots[1] = y#y1

    dots[2] = x + w#x2
    dots[3] = y

    dots[4] = x + w#x3
    dots[5] = y + h#y3

    dots[6] = x
    dots[7] = y + h
    return dots

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labelTxt', default=r'G:\Data\CarPlane\planeRec', type=str)
    parser.add_argument('--FormatRec', default=r'G:\Data\CarPlane\FormatPlaneRec', type=str)
    parser.add_argument('--autocheck', default=r'E:\Data\jilin\autocheck\\', type=str)
    args = parser.parse_args()
    list = GetFile.GetFileFromThisRootDir(args.labelTxt, 'txt');
    outpath = args.FormatRec

    for file in list:
        print('txt', file)
        f = open(file, 'r')

        strlist = file.split('\\');
        print('strlist', strlist)


        filename = strlist[len(strlist) - 1];
        suffix = os.path.splitext(filename)[1]
        print('suffix', suffix)
        filename = filename[0:(len(filename) - len(suffix))];


        outname = os.path.join(outpath, filename + suffix)
        print('outname', outname)
        #out = codecs.open(outname, 'w', 'utf_16')
        while True:
            line = f.readline()
            if line:
                print(line)
                line = line.strip()
                linelist = line.split(' ')
                for index, item in enumerate(linelist):
                    linelist[index] = int(float(item))
                rect = linelist[1:5]
                print('rect', rect)
                dots = recto4dot(rect)
                outline = ''
                for i in range(7):
                    outline = outline + str(dots[i]) + ' '
                outline = outline + str(dots[7])
                print(outline)
                #out.write(outline + '\n')
            else:
                break
        f.close()
        #out.close()
if __name__ == '__main__':
    main()
