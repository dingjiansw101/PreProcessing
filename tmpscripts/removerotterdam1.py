import os
import utils as util

def main():
    names = util.filesetcalc(r'I:\dota2\5du\rotterdam1selectedsub\rotterdam1selectedsub\images',
                            r'I:\dota2\5du\Rotterdam1sub\labelTxt',
                            'd')
    util.filecopy(r'I:\dota2\5du\rotterdam1selectedsub\rotterdam1selectedsub\images',
                  r'I:\dota2\5du\rotterdam1selectedsub\rotterdam1selectedsub\removerotterdamfirstbatch',
                  names,
                  '.jpg')

if __name__ == '__main__':
    main()