import os
import utils as util
import codecs
import shutil

class calcbase():
    def __init__(self):
        releaselist = util.GetFileFromThisRootDir(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\addparkinglabelTxt\labelTxt')
        nextreleaselist = util.GetFileFromThisRootDir(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\addpakinglabelTxt\labelTxt')
        discardreleaselist = util.GetFileFromThisRootDir(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\discard\addparkinglabelTxt\labelTxt')

        countset = {util.mybasename(x.strip()) for x in (releaselist + nextreleaselist)}

    def count(self, srcpath):
        pass


if __name__ == '__main__':
    pass