import os
from  GetFileFromDir import GetFileFromThisRootDir

def main():
    basepath = r'E:\dataset-7.19\dataset-7.19'
    path = os.path.join(basepath, 'labelTxtall')
    list = GetFileFromThisRootDir(path, 'txt')
    for item in list:
        print(item)
    list2 = [x[0:(len(x) - 8)] + '.txt' for x in list]
    list2 = set(list2)
    list3 = []
    for path in list2:
        basename = os.path.basename(path)
        print('basename:', basename)
        if (basename[0] == 'G'):
            list3.append(basename)
    outfilename = os.path.join(basepath, 'gf2.txt')
    out = open(outfilename, 'w')
    for name in list3:
        print(name)
        imgname = os.path.splitext(name)[0]
        out.write(imgname + '\n')
if __name__ == '__main__':
    main()
