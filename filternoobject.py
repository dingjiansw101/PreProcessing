import os
import utils as util


## if not empty return True
def checknotempty(filename):
    objects = util.parse_bod_poly2(filename)
    if (len(objects) == 0):
        return False
    else:
        return True




def removenonobject(srcpath, dstpath):
    srclabel = os.path.join(srcpath, r'labelTxt')
    srclist = util.GetFileFromThisRootDir(srclabel)
    filteredlist = filter(checknotempty, srclist)
    filterednames = [util.mybasename(x) for x in filteredlist]

    util.filecopy(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\images',
                  r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\filtered\images',
                  filterednames,
                  '.jpg')
    util.filecopy(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\labelTxt',
                  r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\filtered\labelTxt',
                  filterednames,
                  '.txt')
    util.filecopy(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\annotations',
                  r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\filtered\annotations',
                  filterednames,
                  '.xml')
if __name__ == '__main__':
    removenonobject(r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches',
                    r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date\nextrelease\patches\filtered')