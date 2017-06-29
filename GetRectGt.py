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

def dotsToRec4(dots):
    xmin, xmax, ymin, ymax = dots[0][0], dots[0][0], dots[0][1], dots[0][1]
    for i in range(3):
        xmin = min(xmin, dots[i+1][0])
        xmax = max(xmax, dots[i+1][0])
        ymin = min(ymin, dots[i+1][1])
        ymax = max(ymax, dots[i+1][1])
    x = (xmin + xmax)/2
    y = (ymin + ymax)/2
    w = xmax - xmin
    h = ymax - ymin
    rec4 = [x, y, w, h]
    return rec4
def dotsToRec8(dots):
    xmin, xmax, ymin, ymax = dots[0][0], dots[0][0], dots[0][1], dots[0][1]
    for i in range(3):
        xmin = min(xmin, dots[i+1][0])
        xmax = max(xmax, dots[i+1][0])
        ymin = min(ymin, dots[i+1][1])
        ymax = max(ymax, dots[i+1][1])
    rec8 = [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]
    return  rec8
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labelTxt', default=r'E:\Data\dataset\trainval\labelTxt', type=str)
    parser.add_argument('--outdir', default=r'E:\Data\dataset\trainval\8dotsRec', type=str)
    parser.add_argument('--outdirRec', default=r'E:\Data\dataset\trainval\4dotsRec', type=str)
    args = parser.parse_args()
    list = GetFile.GetFileFromThisRootDir(args.labelTxt, 'txt');

    for file in list:
        strlist = file.split('\\');
        filename = strlist[len(strlist) - 1]
        suffix = os.path.splitext(filename)[1]
        filename = filename[0:(len(filename) - len(suffix))];
        print('yes', filename)
        f = open(file, 'r', encoding='utf_16')
        outdir = os.path.join(args.outdir, filename + '.txt');
        outdirRec = os.path.join(args.outdirRec, filename + '.txt')

        out4 = codecs.open(outdirRec, 'w', 'utf_16');
        out8 = codecs.open(outdir, 'w', 'utf_16');
        while True:
            dots = []
            line = f.readline()

            if line:
                line = line.strip()
                linelist = line.split(' ')
                print('linelist', linelist)
                dots.append([int(linelist[0]), int(linelist[1])])
                dots.append([int(linelist[2]), int(linelist[3])])
                dots.append([int(linelist[4]), int(linelist[5])])
                dots.append([int(linelist[6]), int(linelist[7])])
                rec4 = dotsToRec4(dots)
                rec8 = dotsToRec8(dots)
                outline4 = ''
                for i in range(4):
                    outline4 = outline4 + str(rec4[i]) + ' '
                for i in range(8, (len(linelist))):
                    outline4 = outline4 + linelist[i]
                print('out4', outline4)
                out4.write(outline4 + '\n')

                outline8 = ''
                for i in range(8):
                    outline8 = outline8 + str(rec8[i]) + ' '
                for i in range(8, len(linelist)):
                    outline8 = outline8 + linelist[i]
                print('out8', outline8)
                #out8.write(line + '\n')
                out8.write(outline8 + '\n')
            else:
                break
        f.close()
if __name__ == '__main__':
    main()