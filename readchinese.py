#coding:utf-8
import os
import codecs,sys
import cv2
import string
import re
import math
import numpy as np

txt = "G:\Data\91Google\dingjian\矩形区域(11)\Level18\矩形区域(11).txt"
f = open(txt, 'r')
while True:
    line = f.readline();
    if line:
        print('line', line)
        if (line[0] == '空'):
            print('get!!!!!!!')
    else:
        break;
f.close()