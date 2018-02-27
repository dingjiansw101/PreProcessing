import os
import utils as util

def readName2Id():
    filename = r'I:\dota\Name2Id.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()
        Name2IdDict = {line.strip().split(':')[0]:line.strip().split(':')[1] for line in lines}
    return Name2IdDict

def resultName2Id(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    Name2IdDict = readName2Id()
    for filename in filelist:
        with open(filename, 'r') as f:
            lines = f.readlines()
            splitlines = [x.strip().split(' ') for x in lines]
            basename = util.mybasename(filename)
            dstname = os.path.join(dstpath, basename + '.txt')
            with open(dstname, 'w') as f_out:
                # for splitline in splitlines:
                #     name = splitline[0]
                #     Id = Name2IdDict[name]
                #     outline = Id + ' ' + ' '.join(splitline[1:])
                #     f_out.write(outline + '\n')
                for i in range(len(splitlines)):
                    splitline = splitlines[i]
                    name = splitline[0]
                    Id = Name2IdDict[name]
                    outline = Id + ' ' + ' '.join(splitline[1:])
                    f_out.write(outline + '\n')
if __name__ == '__main__':
    resultName2Id(r'E:\bod-dataset\results\faster-rcnn-rot-59\nms0.1\comp4_test_nms_0.1',
                  r'E:\bod-dataset\results\faster-rcnn-rot-59\nms0.1\com4_dota')