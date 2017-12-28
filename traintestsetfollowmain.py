import os
import utils as util

def getallset():
    path = r'E:\bod-dataset\labelTxt'
    filelist = util.GetFileFromThisRootDir(path)
    namelist = [util.mybasename(x) for x in filelist]
    return namelist
def rewriteSet(filename):
    allset = getallset()
    with open(filename, 'r') as f:
        lines = f.readlines()
        names = [x.strip() for x in lines]
        outname = os.path.splitext(filename)[0] + '_fix.txt'
        with open(outname, 'w') as f_out:
            for name in names:
                if name in allset:
                    f_out.write(name + '\n')
def main():
    rewriteSet(r'E:\bod-dataset\testset\testset.txt')
    rewriteSet(r'E:\bod-dataset\valset\valset.txt')
    rewriteSet(r'E:\bod-dataset\trainset\trainset.txt')

if __name__ == '__main__':
    main()