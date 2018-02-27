import os
import utils as util
import codecs

def dota2bod(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for filename in filelist:
        basename = util.mybasename(filename)
        dstname = os.path.join(dstpath, basename + '.txt')
        with codecs.open(dstname, 'w', 'utf_16') as f_out:
            objects = util.parse_dota_poly2(filename)
            for obj in objects:
                poly = obj['poly']
                name = obj['name']
                difficult = obj['difficult']
                outline = ' '.join(map(str, poly)) + ' ' + name + ' ' + difficult
                f_out.write(outline + '\n')

if __name__ == '__main__':
    dota2bod(r'I:\dota\trainset\dotalabel',
             r'I:\dota\trainset\labelTxt')

