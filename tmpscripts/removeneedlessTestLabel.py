import os
import utils as util

def getlistfromset(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        names = [x.strip() for x in lines]
    return names
def main():
    names = getlistfromset(r'E:\bod-dataset\testset\testset.txt')
    util.filecopy(r'E:\bod-dataset\testset\labelTxt',
                  r'E:\bod-dataset\testset\labelTxt2',
                  names,
                  '.txt')
if __name__ == '__main__':
    main()
