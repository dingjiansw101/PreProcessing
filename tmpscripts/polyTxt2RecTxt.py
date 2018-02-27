import os
import utils as util
import codecs

def readName2Id():
    filename = r'I:\dota\Name2Id.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()
        Name2IdDict = {line.strip().split(':')[0]:line.strip().split(':')[1] for line in lines}
    return Name2IdDict

def polyTxt2RecTxt(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    Name2IdDict = readName2Id()
    for filename in filelist:
        # with open(filename) as f:
        #     lines = f.readlines()
        #     splitlines = [x.strip().splitlines(' ') for x in lines]
        #     labelLines = splitlines[2:]
        #     for splitline in labelLines:
        objects = util.parse_dota_poly(filename)
        basename = util.mybasename(filename)
        # Id = Name2IdDict[basename]
        with codecs.open(os.path.join(dstpath, basename + '.txt'), 'w') as f_out:
            for obj in objects:
                poly = obj['poly']
                category = obj['name']
                difficult = obj['difficult']
                # if (difficult != '0') or (difficult != '1')
                rect = util.dots4ToRec8(poly)
                ouline = ' '.join(map(str, rect)) + ' ' + category + ' ' + difficult
                f_out.write(ouline + '\n')

if __name__ == '__main__':
    polyTxt2RecTxt(r'I:\dota\testset\dotalabel',
                   r'I:\dota\testset\ReclabelTxt-utf-8')