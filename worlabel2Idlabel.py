import utils as util
import os
import codecs

datamap_15 = {'0A': 'plane', '0B':'plane', '0C': 'plane',  '1': 'baseball-diamond', '2': 'bridge', '3': 'ground-track-field', '4A': 'small-vehicle', '4B': 'large-vehicle',
           '4C': 'large-vehicle', '5A': 'ship', '5B':'ship', '6': 'tennis-court', '7': 'basketball-court',
           '8': 'storage-tank', '9': 'soccer-ball-field', '10': 'turntable',
           '11': 'harbor', '14': 'swimming-pool',
           '16': 'helicopter'}
datamap_inverse = {datamap_15[x]:x for x in datamap_15}
print('datamap_inverse:', datamap_inverse)

def word2id(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    for fullname in filelist:
        print('')
        objects = util.parse_bod_poly2(fullname)
        basename = util.mybasename(fullname)
        outname = os.path.join(dstpath, basename + '.txt')
        print('outname: ', outname)
        with codecs.open(outname, 'w', 'utf_16') as f_out:
            for obj in objects:
                wordname = obj['name']
                idname = datamap_inverse[wordname]
                outline = ' '.join(map(str, obj['poly'])) + ' ' + idname
                f_out.write(outline + '\n')
if __name__ == '__main__':
    word2id(r'E:\bod-dataset\results\faster-rcnn-rot-59\wordlabel',
            r'E:\bod-dataset\results\faster-rcnn-rot-59\labelTxt')