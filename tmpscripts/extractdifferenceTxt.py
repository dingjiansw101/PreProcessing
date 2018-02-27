import os
import utils as util
import operations

def main():
    imagepath = r'I:\dota2\5du\checked\ship2\images'
    labelpath = r'I:\dota2\5du\checked\ship2\labelTxt'
    outpath = r'I:\dota2\5du\checked\ship2\labelTxtdifference'
    diffnames = util.filesetcalc(labelpath, imagepath, 'd')
    operations.filemove(labelpath, outpath, diffnames, '.txt')

if __name__ == '__main__':
    main()