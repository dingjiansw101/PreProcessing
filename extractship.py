import utils as util
import os
import codecs

shipid = ['5A', '5B']

def countship(objects):
    count = 0
    for obj in objects:
        if obj['name'] in shipid:
            count = count + 1
    return count

def filter(srclist):
    outlist = []
    numfile = len(srclist)
    maxnum = int(0.8 * numfile)
    currentnum = 0
    for fullname in srclist:
        objects = util.parse_bod_poly2(fullname)
        shipnum = countship(objects)
        if (currentnum > maxnum):
            break
        if (shipnum > 5):
            currentnum = currentnum + 1
            outlist.append(fullname)
    return outlist

if __name__ == '__main__':
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\labelTxt')

    shiplist = filter(filelist)
    for fullname in shiplist:
        basename = util.mybasename(fullname)
        objects = util.parse_bod_poly2(fullname)
        with codecs.open(os.path.join(r'E:\bod-dataset\ship\labelTxt', basename + '.txt'), 'w', 'utf_16') as f_out:
            for obj in objects:
                if obj['name'] in shipid:
                    outline = ' '.join(map(str, obj['poly'])) + ' ' + obj['name'] + ' ' + obj['difficult']
                    f_out.write(outline + '\n')
    shipbasenames = [util.mybasename(x.strip()) for x in shiplist]
    # util.filecopy(r'E:\bod-dataset\images',
    #               r'E:\bod-dataset\ship\images',
    #               shipbasenames,
    #               r'.png')