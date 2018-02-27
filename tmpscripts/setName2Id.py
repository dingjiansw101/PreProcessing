import os
import utils as util

def readName2Id():
    filename = r'I:\dota\Name2Id.txt'

    with open(filename, 'r') as f:
        lines = f.readlines()
        Name2IdDict = {line.strip().split(':')[0]:line.strip().split(':')[1] for line in lines}
    return Name2IdDict

def main():
    Name2IdDict = readName2Id()
    srcfilename = r'I:\dota\trainset\Nametrainset.txt'
    dstfilename = r'I:\dota\trainset\trainset.txt'
    with open(srcfilename, 'r') as f:
        with open(dstfilename, 'w') as f_out:
            lines = f.readlines()
            lines = [x.strip() for x in lines]
            for line in lines:
                outline = Name2IdDict[line]
                f_out.write(outline + '\n')

if __name__ == '__main__':
    main()