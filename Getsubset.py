import utils as util
import os
import shutil
import random

#def parsewrite(dir, patchdir, )

def subfilter(srcfile, dstfile):
    with open(dstfile, 'w') as f_out:
        with open(srcfile, 'r') as f:
            lines = f.readlines()
            splitlines = [x.strip() for x in lines]
            random.shuffle(splitlines)
            number = len(splitlines)
            subset_number = number / 3
            for i in range(subset_number):
                f_out.write(splitlines[i] + '\n')

def trainfilter(patchfile, dstfile):
    trainsetfile = r'/data/Data_dj/data/bod-v3/subset/trainset.txt'
    valsetfile = r'/data/Data_dj/data/bod-v3/subset/valset.txt'
    with open(trainsetfile, 'r') as f:
        lines = f.readlines()
        trainlist = [x.strip() for x in lines]
    with open(valsetfile, 'r') as f:
        lines = f.readlines()
        vallist = [x.strip() for x in lines]
    trainvalset = set(trainlist).union(set(vallist))

    with open(patchfile, 'r') as f:
        lines = f.readlines()
        patchlist = [util.mybasename(x.strip()) for x in lines]
    patchset = set(patchlist)

  #  print('trainvalset: ', trainvalset)
   # print('patchset: ', patchset)
    with open(dstfile, 'w') as f_out:
        for patch in patchset:
            splitname = patch.split('__')
            # print('splitname: ', splitname)
            oriname = splitname[0]
            if oriname in trainvalset:
                f_out.write(os.path.join(r'/data/Data_dj/data/bod-v3/JPEGImages', patch) + '\n')

def testfilter(patchfile, dstfile):
    testfile = r'/data/Data_dj/data/bod-v3/subset/testset.txt'
    with open(testfile, 'r') as f:
        lines = f.readlines()
        testlist = [x.strip() for x in lines]
    testset = set(testlist)
    with open(patchfile, 'r') as f:
        lines = f.readlines()
        patchlist = [util.mybasename(x.strip()) for x in lines]
    patchset = set(patchlist)
    with open(dstfile, 'w') as f_out:
        for patch in patchset:
            splitname = patch.split('__')
            # print('splitname: ', splitname)
            oriname = splitname[0]
            if oriname in testset:
                f_out.write(os.path.join(r'/data/Data_dj/data/bod-v3/JPEGImages', patch) + '\n')
def main():
    path = r'/data/Data_dj/data/bod-v3'

if __name__ == '__main__':
    # subfilter(r'/data/Data_dj/data/bod-v3/trainset.txt',
    #           r'/data/Data_dj/data/bod-v3/subset/trainset.txt')
    # subfilter(r'/data/Data_dj/data/bod-v3/testset.txt',
    #           r'/data/Data_dj/data/bod-v3/subset/testset.txt')
    # subfilter(r'/data/Data_dj/data/bod-v3/valset.txt',
    #           r'/data/Data_dj/data/bod-v3/subset/valset.txt')
    trainfilter(r'/data/Data_dj/data/bod-v3/train.txt',
                r'/data/Data_dj/data/bod-v3/subset/train.txt')

    testfilter(r'/data/Data_dj/data/bod-v3/test.txt',
               r'/data/Data_dj/data/bod-v3/subset/test.txt')