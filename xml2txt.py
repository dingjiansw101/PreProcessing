import os
import utils
import argparse
from GetFileFromDir import GetFileFromThisRootDir
import codecs

def testlabelme2txt():
    basepath = r'E:\GAOFEN2\gaofen2Labelme'
    utils.labelme2txt(basepath)

if __name__ == '__main__':
    testlabelme2txt()