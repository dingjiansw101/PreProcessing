import os
import cv2
import argparse
from GetFileFromDir import GetFileFromThisRootDir

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgdir', default=r'/home/ding/data/GFJL/splitdir/images', type=str)
    parser.add_argument('--jpgimgdir', default=r'/home/ding/data/GFJL/splitdir/jpgimgs', type=str)
    args = parser.parse_args()

    imgnames = GetFileFromThisRootDir(args.imgdir)
    for imgname in imgnames:
        img = cv2.imread(imgname)
        basename = os.path.basename(imgname)
        suffix = os.path.splitext(basename)[1]
        name = basename[0:len(basename) - len(suffix)]
        outdir = os.path.join(args.jpgimgdir, name + '.jpg')
        print('imgname', imgname)
        print('outdir', outdir)
        cv2.imwrite(outdir, img)
if __name__ == '__main__':
    main()