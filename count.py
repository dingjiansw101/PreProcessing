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
def main():
    parser = argparse.ArgumentParser()
    basepath  = r'E:\GoogleEarth\up-9-25-data\secondjpg\trainsplit'
    clearlabelpath = os.path.join(basepath, 'clearlabelTxt')
    parser.add_argument('--labelTxt', default=os.path.join(basepath, 'labelTxt'), type=str)
    parser.add_argument('--autocheck', default=os.path.join(basepath, 'autocheck'), type=str)
    args = parser.parse_args()
    list = GetFileFromThisRootDir(args.labelTxt, 'txt');
    basedir = args.autocheck
    print(basedir)
    problem = os.path.join(basedir, 'problem.txt')
    print('problem', problem)
    pro_out = open(problem, 'w')
    for txt in list:
        print('txt', txt)
        f = open(txt, 'r', encoding='utf_16')
        filename = os.path.basename(os.path.splitext(txt)[0])
        count = 0;
        print(txt)
        ## optional out
        #outname = os.path.join(clearlabelpath, filename + '.txt')
        #f_out = codecs.open(outname, 'w', 'utf_16')
        while True:
            count = count + 1
            line = f.readline()
            if line:
                line = line.strip()
                linelist = line.split(' ')
                print('linelist', linelist)
                if (len(linelist) <= 8):
                    pro_out.write(filename + ' line: ' + str(count) + ' missing label' + '\n')
                else:
                    if (linelist[8] not in clsdict) :
                        pro_out.write(filename + ' line: ' + str(count) + ' wrong label: ' + str(linelist[8]) + '\n')
                    else:
                        clsdict[linelist[8]] = clsdict[linelist[8]] + 1
                        #f_out.write(line + '\n')
            else:
                break
        f.close()
    pro_out.close()
    print('class', clsdict)
    count_dir = os.path.join(basedir, 'count.txt')
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
        print('id: ', id)
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
