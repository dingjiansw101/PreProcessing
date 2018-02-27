import cv2
import os
import utils as util
import shutil

def copywithNameChange(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    names = [util.mybasename(x) for x in filelist]
    with open(os.path.join(r'I:\dota', r'Name2Id.txt'), r'w') as f_out:
        for index, name in enumerate(names):
            id = 'P' + str(index).zfill(4)
            srcname = os.path.join(srcpath, name + '.png')
            if name == 'Thumbs':
                continue
            dstname = os.path.join(dstpath, id + '.png')
            if not os.path.exists(dstname):
                shutil.copyfile(srcname, dstname)
            outline = name + ':' + id
            f_out.write(outline + '\n')
if __name__ == '__main__':
    copywithNameChange(r'E:\bod-dataset\images',
                       r'I:\dota\pngs')