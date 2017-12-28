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



def main():
    path = r'G:\Data\中科院大学高清航拍目标数据集合\中科院大学高清航拍目标数据集合\PLANE'
    list = GetFile.GetFileFromThisRootDir(path, 'txt')
    outpath = r'G:\Data\中科院大学高清航拍目标数据集合\中科院大学高清航拍目标数据集合\planetxt'
    for file in list:
        print('txt', file)
        f = open(file, 'r')
        strlist = file.split('\\');
        print('strlist', strlist)
        filename = strlist[len(strlist) - 1];
        print('filename', filename)
        dir = os.path.join(outpath, filename)
        out = codecs.open(dir, 'w', 'utf_16');
        while True:
            line = f.readline()
            if line:
                line = line.strip()
                linelist = line.split('\t');
                for index, item in enumerate(linelist):
                    patch = item.split('e+')
                    print('patch', patch)
                    left = float(patch[0])
                    if (len(patch) == 2):
                        right = float(patch[1])
                    else:
                        right = 1
                    linelist[index] = left * math.pow(10, right)
                outline = ''
                for i in range(0, 7):
                    outline = outline + str(int(linelist[i])) + ' '
                outline = outline + str(linelist[7])
                out.write(outline + '\n')
            else:
                break
        f.close()
        out.close()
if __name__ == '__main__':
    main()