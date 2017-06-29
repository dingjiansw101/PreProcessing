#coding:utf-8
import os
import numpy as np
import codecs,sys
import txtsplit
from  GetFileFromDir import GetFileFromThisRootDir
class object:
    bbox = np.zeros(8) - 1;
    label = -1;
    hardflag = -2;
test = []
ob1 = object()
ob1.bbox = object.bbox + 3;
ob2 = object()
test.append(ob1)
test.append(ob2)
print(test[0].bbox)
print(test[1].bbox)

while True:
    pass
list = GetFileFromThisRootDir('G:\oldtonew\oldtxt', 'txt');
basedir = 'G:\oldtonew\\newtxt\\';
print(basedir)
for txt in list:
    print(txt)
    txtsplit.txtsplit(txt, basedir)
print(object)