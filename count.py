#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math
import numpy as np

def GetFileFromThisRootDir(dir,ext = None):
  allfiles = []
  needExtFilter = (ext != None)
  for root,dirs,files in os.walk(dir):
    for filespath in files:
      filepath = os.path.join(root, filespath)
      extension = os.path.splitext(filepath)[1][1:]
      if needExtFilter and extension in ext:
        allfiles.append(filepath)
      elif not needExtFilter:
        allfiles.append(filepath)
  return allfiles

list = GetFileFromThisRootDir('G:\标注2\summary\labelTxt', 'txt');
basedir = 'G:\标注2\summary\count\\';
print(basedir)
problem = basedir + 'problem.txt'
pro_out = open(problem, 'w');
cls = np.zeros(11, dtype=np.int32)
print('cls', cls)

for txt in list:
    print('txt', txt)
    f = open(txt, 'r', encoding='utf_16')
    dir = basedir + 'count.txt'

    strlist = txt.split('\\');
    filename = strlist[len(strlist) - 1];
    filename = filename[0:(len(filename) - 4)];
    print('yes', filename);

    cnt = 0;
    allcnt = 0;
    print(txt)
    flag = 0;
    label = -1;# -1 represtnt nothing

    while True:
        line = f.readline()
        if line:
            line = line.strip()
            linelist = line.split(' ')
            print('linelist', linelist)
            for index, item in enumerate(linelist):
                linelist[index] = int(item)
            print('linelist', linelist)

            if (len(linelist) <= 8):
                pro_out.write(filename + ' missing label' + '\n')
            elif (linelist[8] > 10):
                pro_out.write(filename + ' wrong label' + '\n')

            if len(linelist) >= 9:
                if linelist[8] <= 10:
                    cls[linelist[8]] = cls[linelist[8]] + 1
        else:
            break
    f.close()
print('class', cls)
print('sum', cls.sum())