import os
import utils as util

# def groundtruth2Task2(srcpath, dstpath):
#     filelist = util.GetFileFromThisRootDir(srcpath)
#     # filelist = util.GetFileFromThisRootDir(r'I:\dota\testset\ReclabelTxt-utf-8')
#     for filename in filelist:
#         objects = util.parse_dota_poly(filename)
#         basename = util.mybasename(filename)
#         with open(os.path.join(dstpath, basename + '.txt')):
#             for obj in objects:
#                 poly = obj['poly']
#                 category = obj['name']

def main():

    testlistfile = r'I:\dota\testset\testset.txt'
    with open(testlistfile, 'r') as f:
        lines = f.readlines()
        namelist = []
        for line in lines:
            namelist.append(line.strip())
    filedict = {}
    for cls in util.wordname_15_new:
        fd = open(os.path.join(r'I:\dota\testset\Task1format_gt', r'Task1_' + cls + r'.txt'), r'w')
        filedict[cls] = fd

    for name in namelist:
        filepath = os.path.join(r'I:\dota\testset\dotalabel', name + '.txt')
        objects = util.parse_dota_poly2(filepath)
        for obj in objects:
            category = obj['name']
            poly = obj['poly']
            difficult = int(obj['difficult'])
            #print('difficult:', difficult)
            #if not difficult:
            # bbx = util.dots4ToRec4(poly)
            outline = name + ' ' + '1' + ' '  + ' '.join(map(str, poly))
            filedict[category].write(outline + '\n')


if __name__ == '__main__':
    main()