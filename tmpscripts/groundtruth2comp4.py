import os
import utils as util




def main():

    testlistfile = r'I:\dota\testset\fordebug\debugset.txt'
    with open(testlistfile, 'r') as f:
        lines = f.readlines()
        namelist = []
        for line in lines:
            namelist.append(line.strip())
    filedict = {}
    for cls in util.wordname_15:
        fd = open(os.path.join(r'I:\dota\testset\fordebug\Taskformat_gt', r'Task1_' + cls + r'.txt'), r'w')
        filedict[cls] = fd

    for name in namelist:
        filepath = os.path.join(r'I:\dota\testset\fordebug\labelTxt', name + '.txt')
        objects = util.parse_bod_poly(filepath)
        for obj in objects:
            category = obj['name']
            poly = obj['poly']
            difficult = int(obj['difficult'])
            #print('difficult:', difficult)
            #if not difficult:
            bbx = util.dots4ToRec4(poly)
            outline = name + ' ' + '1' + ' '  + ' '.join(map(str, bbx))
            filedict[category].write(outline + '\n')


if __name__ == '__main__':
    main()