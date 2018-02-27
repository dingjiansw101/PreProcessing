import os
import utils as util

def check(srcpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for filename in filelist:
        objects = util.parse_dota_poly(filename)
        for obj in objects:
            category = obj['name']
            difficult = obj['difficult']
            if (difficult != '0') and (difficult != '1'):

                print('filename:', filename)
                print('difficult:', difficult)
            area = obj['area']
            if (area <= 0):
                print('filename:', filename)
                print('area:', area)
if __name__ == '__main__':
    check(r'I:\dota\testset\dotalabel')