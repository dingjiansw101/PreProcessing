import os
import utils as util
import codecs

def readName2Id():
    filename = r'I:\dota\Name2Id.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()
        Name2IdDict = {line.strip().split(':')[0]:line.strip().split(':')[1] for line in lines}
    return Name2IdDict
def main():
    filelist = util.GetFileFromThisRootDir(r'I:\dota\wordlabelMS')
    Name2IdDict = readName2Id()
    dstpath = r'I:\dota\dotalabelutf-8'
    #dstpath = r'I:\dota\dotalabelutf-16'
    for filename in filelist:
        basename = util.mybasename(filename)
        resname = os.path.join(r'E:\bod-dataset\resolution', basename + '.txt')
        print('resname:', resname)
        if not os.path.exists(resname):
            resolution = 'null'
        else:
            with open(resname, 'r') as f:
                lines = f.readlines()
                if len(lines) == 0:
                    resolution = 'null'
                else:
                    resolution = lines[0].strip()
        objects = util.parse_bod_poly2(filename)
        Idname = Name2IdDict[basename]
        with codecs.open(os.path.join(dstpath, Idname + '.txt'), r'w') as f_out:

            if (basename[0:2] == r'JL'):
                imagesource = 'JL'
            elif (basename[0:2] == r'GF'):
                imagesource = 'GF'
            else:
                imagesource = 'GoogleEarth'
            outline = 'imagesource:' + imagesource
            f_out.write(outline + '\n')
            outline = 'gsd:' + resolution
            f_out.write(outline + '\n')
            for obj in objects:
                poly = obj['poly']
                name = obj['name']
                difficult = obj['difficult']
                outline = ' '.join(map(str, poly)) + ' ' + name + ' ' + difficult
                f_out.write(outline + '\n')
if __name__ == '__main__':
    main()