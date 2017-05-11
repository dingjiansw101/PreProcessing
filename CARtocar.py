#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math

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

list = GetFileFromThisRootDir('G:\Data\中科院大学高清航拍目标数据集合\中科院大学高清航拍目标数据集合\PLANE', 'txt');
basedir = 'G:\Data\中科院大学高清航拍目标数据集合\中科院大学高清航拍目标数据集合\planeRec\\';
print(basedir)


for txt in list:
    print('txt', txt)
    f = open(txt, 'r')
    #f = open(txt, 'r');
    strlist = txt.split('\\');
    #print('yes', strlist[len(strlist) - 1])
    filename = strlist[len(strlist) - 1];
    filename = filename[0:(len(filename) - 4)];
    print('yes', filename);
    dir = basedir + filename + '.txt';
    #out = codecs.open(dir, 'w', 'utf_16');
    out = codecs.open(dir, 'w')
    cnt = 0;
    allcnt = 0;
    print(txt)
    flag = 0;
    label = -1;# -1 represtnt nothing

    while True:
        line = f.readline()
        if line:
            #print(line)
            line = line.strip()
            #print('line', line)
            linelist = line.split('\t');
            #print('10', int('10e+1'))
            for index, item in enumerate(linelist):
                patch = item.split('e+')
                print('patch', patch)
                left = float(patch[0])
                if (len(patch) == 2):
                    right = float(patch[1])
                else:
                    right = 1
                linelist[index] = left * math.pow(10, right)
                #print('num', num)
            outline = '1 '
            print('linelist', linelist)
            linelist[9] = linelist[9] + linelist[11]/2
            linelist[10] = linelist[10] + linelist[12]/2
            for i in range(9, 12):
                outline = outline + str(int(linelist[i])) + ' '
            outline = outline + str(linelist[12])
            out.write(outline + '\n')
        else:
            break
    f.close()