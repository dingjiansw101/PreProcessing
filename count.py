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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--labelTxt', default=r'E:\GoogleEarth\杜阳\杜阳8.5\杜阳8.5\labelTxt', type=str)
    parser.add_argument('--autocheck', default=r'E:\GoogleEarth\杜阳\杜阳8.5\杜阳8.5\autocheck\\', type=str)
    args = parser.parse_args()
#    list = GetFileFromThisRootDir(r'G:\Data\91Google\zhouduoyou\5.9\5.9\labelTxt', 'txt');
    list = GetFileFromThisRootDir(args.labelTxt, 'txt');
    #basedir = r'G:\Data\91Google\zhouduoyou\5.9\5.9\autocheck\\'
    basedir = args.autocheck
    print(basedir)
    problem = os.path.join(basedir, 'problem.txt')
    print('problem', problem)
    pro_out = open(problem, 'w')
    dataDic = { '0A': 'passenger plane', '0B': 'fighter aeroplane', '0C': 'radar warning aircraft',
               '1': 'baseball diamond', '2': 'bridge', '3': 'ground track', '4A': 'car', '4B': 'truck',
               '4C': 'bus', '5A': 'ship', '5': 'ship', '5B': 'warship', '6': 'tennis court', '7': 'Basketball court',
               '7B': 'half basketball', '8': 'storage tank', '9': 'soccer ball field', '10': 'Turntable',
               '11': 'harbor', '12': 'electric pole', '13': 'parking lot', '14': 'swimming pool', '15': 'lake',
               '16': 'helicopter', '17': 'airport', '18A': 'viaduct', '18B': '18B', '18C': '18C', '18D': '18D',
               '18E': '18E', '18F': '18F', '18G': '18G', '18H': '18H', '18I': '18I', '18J': '18J', '18K': '18K',
               '18L': '18L', '18M': '18M', '18N': '18N', '4A_area': '4A_area', '4B_area': '4B_area',
               '5A_area': '5A_area', '8_area': '8_area', '13_area': '13_area', 'bridge': 'bridge', 'plane': 'plane',
               'ship': 'ship', 'storage': 'storage', 'harbor': 'harbor'}

    classname = ['0A', '0B', '0C', '1', '2', '3', '4A',  '4B', '4C', '5A', '5B', '6', '7', '8', '9', '10'
               , '11', '12', '13', '14', '15', '16', '17', '18A', '18B', '18C', '18D', '18E'
               , '18F', '18G', '18H', '18I', '18J', '18K', '18L', '18M', '18N', '5', 'plane', 'ship', 'storage', 'bridge', 'harbor']
    clsdict = {'0A':0, '0B':0, '0C':0,  '1':0, '2':0, '3':0, '4A':0,  '4B':0, '4C':0, '5A':0, '5B':0, '6':0, '7':0, '8':0, '9':0, '10':0
               , '11':0, '12':0, '13':0, '14':0, '15':0, '16':0, '17':0, '18A':0, '18B':0, '18C':0, '18D':0, '18E':0
               , '18F':0, '18G':0, '18H':0, '18I':0, '18J':0, '18K':0, '18L':0, '18M':0, '18N':0, '5':0
               ,'plane':0, 'ship':0, 'storage':0, 'bridge':0, 'harbor':0}
    for txt in list:
        print('txt', txt)
        f = open(txt, 'r', encoding='utf_16')
        #f = open(txt, 'r')
        #dir = basedir + 'count.txt'
        strlist = txt.split('\\');
        filename = strlist[len(strlist) - 1];
        filename = filename[0:(len(filename) - 4)];
        print('yes', filename)
        count = 0;
        print(txt)
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
            else:
                break
        f.close()
    pro_out.close()
    print('class', clsdict)
    dir = basedir + 'count.txt'
    count_out = open(dir, 'w')
    sum = 0
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
