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
#from utils import datamap_15 as dataDic
#from utils import classname_15 as classname
from utils import classnums_15 as classnums
from plot import plotbar
import utils as util
## TODO: add crosspass
def main():
    parser = argparse.ArgumentParser()
    basepath  = r'E:\bod-dataset'
    parser.add_argument('--labelTxt', default=os.path.join(basepath, 'wordlabel'), type=str)
    parser.add_argument('--autocheck', default=os.path.join(basepath, 'autocheck', 'by-word'), type=str)
    args = parser.parse_args()
    list = GetFileFromThisRootDir(args.labelTxt, 'txt');
    basedir = args.autocheck
    problem = os.path.join(basedir, 'problem.txt')
    pro_out = open(problem, 'w')
    count_orientation = 0
    for txt in list:
        with open(txt, 'r', encoding='utf_16') as f:
            filename = os.path.basename(os.path.splitext(txt)[0])
            count = 0;
            lines = f.readlines()
            for line in lines:
                count = count + 1
                splitline = line.strip().split(' ')
                if (len(splitline) <= 8):
                    pro_out.write(filename + ' line: ' + str(count) + ' missing label' + '\n')
                else:
                    if (splitline[8] not in classnums) :
                        pro_out.write(filename + ' line:' + str(count) + ' wrong label: ' + str(splitline[8]) + '\n')
                    else:
                        classnums[splitline[8]] = classnums[splitline[8]] + 1
                    if (len(splitline) == 10) and (splitline[9] == '2'):
                        count_orientation = count_orientation + 1
    pro_out.close()
    count_dir = os.path.join(basedir, 'count.txt')
    count_out = open(count_dir, 'w')
    sum = 0
    names = []
    y = []
    for name in classnums:
         outline = str(name) + ': ' + str(classnums[name])
         count_out.write(outline + '\n')
         sum = sum + classnums[name]
         names.append(name)
         y.append(classnums[name])
    count_out.write('sum: ' + str(sum))
    count_out.close()
    fname = os.path.join(basedir, 'categoryDistribution.png')
    plotbar(names, y, fname)
    print('count_orientation:', count_orientation)
if __name__ == '__main__':
    main()
