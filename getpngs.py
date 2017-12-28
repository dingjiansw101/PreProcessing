import os
import utils as util
import cv2

def main():
    googlepath = r'E:\GoogleEarth\up-9-25-data\secondjpg\most-up-date'
    imgpath = os.path.join(googlepath, 'images')
    files = util.GetFileFromThisRootDir(imgpath)
    chooseimgs = {util.mybasename(x) for x in files}
    origpath = r'E:\GoogleEarth\up-9-25-data'
    orignames = util.GetFileFromThisRootDir(origpath, '.tif')
    outpath = r'E:\bod-dataset\GooglePng'
    translist = []
    for fullname in orignames:
        imgname = util.mybasename(fullname)
        if imgname in chooseimgs:
            print('name: ', imgname)
            if imgname not in translist:
                translist.append(imgname)
                img = cv2.imread(fullname)
                outdir = os.path.join(outpath, imgname + '.png')
                cv2.imwrite(outdir, img)

if __name__ == '__main__':
    main()