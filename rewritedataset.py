import os
import utils as util

filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\jpgs')
names = [util.mybasename(x.strip()) for x in filelist]
print('len:', len(names))
def regetset(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    setnames = [x.strip() for x in lines]
    with open(os.path.splitext(filename)[0] + '_re.txt', 'w') as f_out:
        for name in setnames:
            if name in names:
                f_out.write(name + '\n')
            else:
                print(name)
def test():
    regetset(r'E:\bod-dataset\trainset\trainset.txt')

if __name__ == '__main__':
    trainset = util.GetListFromfile(os.path.join(r'E:\bod-dataset\trainset', 'trainset_re.txt'))
    testset = util.GetListFromfile(os.path.join(r'E:\bod-dataset\testset', 'testset_re.txt'))
    valset = util.GetListFromfile(os.path.join(r'E:\bod-dataset\valset', 'valset_re.txt'))
    allset = valset.union(trainset.union(testset))
    inter1 = trainset.intersection(testset)
    inter2 = trainset.intersection(valset)
    inter3 = testset.intersection(valset)
    print('inter1:', inter1)
    print('inter2:', inter2)
    print('inter3:', inter3)