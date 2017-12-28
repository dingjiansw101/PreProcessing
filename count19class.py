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
from utils import datamap_15 as dataDic
from utils import classname_15 as classname
from utils import classnums_15 as classnums
from plot import plotbar
import utils as util
## TODO: add crosspass
def main():
    parser = argparse.ArgumentParser()
    basepath  = r'E:\bod-dataset\patches\subcategorylabel'
    clearlabelpath = os.path.join(basepath, 'clearlabelTxt')
    parser.add_argument('--labelTxt', default=os.path.join(basepath, 'labelTxt'), type=str)
    parser.add_argument('--autocheck', default=os.path.join(basepath, 'autocheck'), type=str)
    args = parser.parse_args()
    list = GetFileFromThisRootDir(args.labelTxt, 'txt');
    basedir = args.autocheck
    problem = os.path.join(basedir, 'problem.txt')
    pro_out = open(problem, 'w')
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
                    if (splitline[8] not in classname) :
                        pro_out.write(filename + ' line:' + str(count) + ' wrong label: ' + str(splitline[8]) + '\n')
                    else:
                        classnums[dataDic[splitline[8]]] = classnums[dataDic[splitline[8]]] + 1
    pro_out.close()
    count_dir = os.path.join(basedir, 'count.txt')
    count_out = open(count_dir, 'w')
    sum = 0
    ## not pythonic
    names = []
    y = []
    for name in classnums:
         outline = ''
         outline = str(name) + ': ' + str(classnums[name])
         count_out.write(outline + '\n')
         sum = sum + classnums[name]
         names.append(name)
         y.append(classnums[name])
    count_out.write('sum: ' + str(sum))
    count_out.close()
    savepath = r'E:\documentation\dataset\summarytxt'
    fname = os.path.join(savepath, 'categoryDistribution.png')

    plotbar(names, y, fname)
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
