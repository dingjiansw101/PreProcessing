#coding:utf-8
import os
import codecs,sys
import string
import re
import math
import numpy as np
import argparse
from  GetFileFromDir import GetFileFromThisRootDir
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from utils import datamap as dataDic
from utils import classname
from utils import clsdict
import utils as util

def main():
    parser = argparse.ArgumentParser()
    basepath  = r'E:\GoogleEarth\up-9-25-data\SecondQuality\qinshaojie'
    clearlabelpath = os.path.join(basepath, 'clearlabelTxt')
    parser.add_argument('--labelTxt', default=os.path.join(basepath, 'labelTxt'), type=str)
    parser.add_argument('--autocheck', default=os.path.join(basepath, 'autocheck'), type=str)
    args = parser.parse_args()
    list = GetFileFromThisRootDir(args.labelTxt, 'txt');
    basedir = args.autocheck
    print(basedir)
    problem = os.path.join(basedir, 'problem.txt')
#    pro_out = open(problem, 'w')
    for fullname in list:
        objects = util.parse_bod_poly2(fullname)
        basename = os.path.basename(os.path.splitext(fullname)[0])
        for obj in objects:
            long_axis = obj['long-axis']
            if (long_axis > 15) and (obj['name'] in clsdict):
                clsdict[obj['name']] = clsdict[obj['name']] + 1

    count_dir = os.path.join(basedir, 'count_exclude_verysmall.txt')
    count_out = open(count_dir, 'w')
    sum = 0
    ## not pythonic
    for item in classname:
         outline = ''
         wordname = dataDic[item]
         #outline = str(item) + ': ' + str(clsdict[item])
         outline = str(wordname) + ': ' + str(clsdict[item])
         count_out.write(outline + '\n')
         sum = sum + clsdict[item]
    count_out.write('sum: ' + str(sum))
    count_out.close()
    names = []
    y = []
    for id in clsdict:
        #print('id: ', id)
        name = dataDic[id]
        names.append(name)
        number = clsdict[id]
        y.append(number)
    # x = range(len(names))
    # plt.plot(x, y, 'ro-')
    # plt.xticks(x, names, rotation=45)
    # plt.margins(0.06)
    # plt.subplots_adjust(bottom=0.15)
    # print('before show')
    # plt.show()
    # plt.savefig()
    # print('after show')
if __name__ == '__main__':
    main()
