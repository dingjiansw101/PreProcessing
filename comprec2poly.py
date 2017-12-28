import os
import utils as util

def box2poly(bbox):
    xmin, ymin, xmax, ymax = bbox[0], bbox[1], bbox[2], bbox[3]
    poly = [xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]
    return poly
def Trans(srcpath, dstpath):
    filelist = util.GetFileFromThisRootDir(srcpath)
    namelist = [util.mybasename(name) for name in filelist]
    for fullname in namelist:
        srcname = os.path.join(srcpath, fullname + '.txt')
        with open(srcname, 'r') as f:
            outname = os.path.join(dstpath, fullname + '.txt')
            with open(outname, 'w') as f_out:
                lines = f.readlines()
                splitlines = [x.strip().split(' ') for x in lines]
                for splitline in splitlines:
                    imgname = splitline[0]
                    score = splitline[1]
                    bbox = splitline[2:]
                    poly = box2poly(bbox)
                    outline = imgname + ' ' + score + ' ' + ' '.join(poly)
                    f_out.write(outline + '\n')

if __name__ == '__main__':
    Trans(r'E:\bod-dataset\results\faster-rcnn-30\nms',
          r'E:\bod-dataset\results\faster-rcnn-30\poly_nms')