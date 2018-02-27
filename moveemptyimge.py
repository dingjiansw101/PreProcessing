import os
import utils as util
import operations as ope

def emptyfilter(srclist):
    dstlist = []
    for filename in srclist:
        objects = util.parse_bod_poly(filename)
        if len(objects) > 1:
            dstlist.append(filename)
    return dstlist

def main():
    srcpath = r'I:\dota2\5du\harbor\Filteredhabor\Filteredharbor2098\images'
    dstapath = r'I:\dota2\5du\harbor\Filteredhabor\Filteredharbor2098\emptyimages'

    filelist = util.GetFileFromThisRootDir(r'I:\dota2\5du\harbor\Filteredhabor\Filteredharbor2098\labelTxt')
    filteredlist = emptyfilter(filelist)
    names = [util.mybasename(x) for x in filteredlist]
    ope.filemove(srcpath, dstapath,
                 names, '.jpg')
if __name__ == '__main__':
    main()