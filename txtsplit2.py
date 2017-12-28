import os
import codecs
import numpy as np
import math
from GetFileFromDir import GetFileFromThisRootDir
import argparse
import cv2
import sympy.geometry as geo
import shapely.geometry as shgeo
import utils as util

parser = argparse.ArgumentParser()
basepath = r'E:\bod-dataset'
parser.add_argument('--gap', default=80, type=int)
parser.add_argument('--subsize', default=1024, type=int)
parser.add_argument('--thresh', default=1, type=float)
args = parser.parse_args()
labeldir = os.path.join(basepath, 'wordlabel')
imagedir = os.path.join(basepath, 'images')

splitlabeldir = os.path.join(basepath, 'patches', 'wordlabel')
splitimagedir = os.path.join(basepath, 'patches', 'images')

outlier1 = 0
outlier2 = 0

#f_error_name = os.path.join(args.dir, 'autocheck', 'error.txt')
#f_error = open(f_error_name, 'w')

with open(os.path.join(basepath, 'patches', 'cutcfg.txt'), 'w') as f_cfg:
    f_cfg.write('gap:' + str(args.gap) + '\n')
    f_cfg.write('subsize:' + str(args.subsize))

## TODO: rm images, the black propotion is very high
def txtsplitpad(imagesize, name, gap, subsize):
    pass
## point: (x, y), rec: (xmin, ymin, xmax, ymax)
def PointInRec(point, rec):
    return (rec[0] <= point[0]) and (point[0] <= rec[2]) and (rec[1] <= point[1]) and (point[1] <= rec[3])

def txtsplit(imagesize, name, gap, subsize):
    #print('imagesize', imagesize)
    ### split the cut txt function return a 2-d list, or a dict, 使用字典， 那个子图有文件才创建, the index(2-dlist) or key(dict) represent the file to create,  and save txt process
    grid_m = int((imagesize[0] - gap)/(subsize - gap))
    grid_n = int((imagesize[1] - gap)/(subsize - gap))
    filelist = []
    for y in range(grid_m + 1):
        filelist.append([])
        for x in range(grid_n + 1):
            subfilename = name + '-' + str(y) + '_' + str(x) + '.txt'
    #        print('splitlabeldir', splitlabeldir)
    #        print('subfilename', subfilename)
            subdir = os.path.join(splitlabeldir, subfilename)
    #        print('txtsubdir', subdir)
            out = codecs.open(subdir, 'w', 'utf_16');
            filelist[y].append(out)

    gtdir = os.path.join(labeldir, name + '.txt')
    f = open(gtdir, 'r', encoding='utf_16')
    #print('imagesize: ', imagesize)
    lines = f.readlines()
    for line in lines:
            linelist = line.strip().split(' ')
            object_strct = {}
            object_strct['bbox'] = list(map(int, linelist[0:8]))
            bbox = object_strct['bbox']
            if len(linelist) == 10:
                if linelist[9] == '1':
                    object_strct['difficult'] = 1
                else:
                    object_strct['difficult'] = 0
            else:
                object_strct['difficult'] = 0;
            if (len(linelist) >= 9):
                object_strct['name'] = linelist[8]
            tmp_set = set()
            ## n correspond to x, m correspond to y
            ## divide by (subsize - gap)
            grids = []
            for i in range(4):
                ggrid_x, ggrid_y = int((object_strct['bbox'][i * 2])/ (subsize - gap)), int((object_strct['bbox'][i * 2 + 1]) / (subsize - gap))
                if (ggrid_x, ggrid_y) not in grids:
                    grids.append((ggrid_x, ggrid_y))
                grid_xp, grid_yp = ggrid_x, ggrid_y
                if ((ggrid_x * (subsize - gap) + gap) > object_strct['bbox'][i * 2]):
                    grid_xp = max(ggrid_x - 1, 0)
                if ((ggrid_y * (subsize - gap) + gap) > object_strct['bbox'][i * 2 + 1] ):
                    grid_yp = max(ggrid_y - 1, 0)
                if (grid_xp, grid_yp) not in grids:
                    grids.append((grid_xp, grid_yp))
            for grid in grids:
                grid_x, grid_y = grid[0], grid[1]
                if (grid_x, grid_y) not in tmp_set:
                    leftup_x = math.floor(grid_x * (subsize - gap))
                    leftup_y = math.floor(grid_y * (subsize - gap))
                    rightdown_x = leftup_x + subsize
                    rightdown_y = leftup_y + subsize
                    ## common part
                    tmp_bbox = np.zeros(8)
                    for i in range(4):
                        tmp_bbox[i * 2] = int(object_strct['bbox'][i * 2] - leftup_x)
                        tmp_bbox[i * 2 + 1] = int(object_strct['bbox'][i * 2 + 1] - leftup_y)

                   # print('writing...')
                    outline = ' '.join(list(map(str, tmp_bbox)))
                    if 'name' in object_strct:
                        #print('name:', object_strct['name'])
                        outline = outline + ' ' + object_strct['name'] + ' '
                    if (object_strct['difficult']):
                        outline = outline + str(1)
                    ## if we don't want the trunated ground truth, set thresh as 1
                    imgpoly = shgeo.Polygon([(leftup_x, leftup_y), (rightdown_x, leftup_y), (rightdown_x, rightdown_y), (leftup_x, rightdown_y)])
                    gtpoly = shgeo.Polygon([(bbox[0], bbox[1]),
                                             (bbox[2], bbox[3]),
                                             (bbox[4], bbox[5]),
                                             (bbox[6], bbox[7])])
                    inter_poly = imgpoly.intersection(gtpoly)
                    inter_area = inter_poly.area
                    gtpoly_area = gtpoly.area
                    half_iou = inter_area/gtpoly_area
                    ## TODO: find the bug, cause grid_x, grid_y out of index
                    if (half_iou >= args.thresh):
                        if (grid_y > grid_m) or (grid_x > grid_n):
                            #f_error.write(name + '\n')
                            global outlier2
                            outlier2 = outlier2 + 1
                        else:
                            filelist[grid_y][grid_x].write(outline + '\n')
                            tmp_set.add((grid_x, grid_y))
                    else:
                        global outlier1
                        outlier1 = outlier1 + 1
    f.close()

def imagesplit(img, imagesize, imgnamedir, gap, subsize):
    ## width -- imagesize[1], height -- imagesize[0]
    grid_m = int(imagesize[0]/(subsize - gap))
    grid_n = int(imagesize[1]/(subsize - gap))
    imgname = os.path.basename(imgnamedir)
    suffix = os.path.splitext(imgname)[1]
    name = imgname[0:(len(imgname) - len(suffix))];
    #print('----------------------start')
    ###
    ## range are big enough
    for y in range(grid_m + 10):
        for x in range(grid_n + 10):
            index_x1 = int((subsize - gap)*x)
            index_x2 = int(index_x1 + subsize)
            index_y1 = int((subsize - gap)*y)
            index_y2 = int(index_y1 + subsize)

            subimg = np.zeros((subsize, subsize, 3))
            index_x2 = min(index_x2, imagesize[1])
            index_y2 = min(index_y2, imagesize[0])
            sub_width, sub_height = index_x2 - index_x1, index_y2 - index_y1
            subimg[0:sub_height, 0:sub_width] = img[index_y1:index_y2,
                                        index_x1:index_x2]
            subname = name + '-' + str(y) + '_' + str(x) + '.jpg'
            subdir = os.path.join(splitimagedir, subname)
            cv2.imwrite(subdir, subimg)
            if (((x + 1) * (subsize - gap) + gap ) >= imagesize[1]):
                break
        if (((y + 1) * (subsize - gap) + gap ) >= imagesize[0]):
            break
    #print('<<<<<<<<<<<<<<<<<<<<<<end')

def splitdata(imgnamedir, gap, subsize):
    img = cv2.imread(imgnamedir)
    imagesize = img.shape
    imgname = os.path.basename(imgnamedir)
    suffix = os.path.splitext(imgname)[1]
    name = imgname[0:(len(imgname) - len(suffix))];
    print('imgname', imgname)
    print('name', name)
    txtsplit(imagesize, name, gap, subsize)
    imagesplit(img, imagesize, imgnamedir, gap, subsize)

def main():

    imagelist = GetFileFromThisRootDir(imagedir);
    count = 0
    for imgname in imagelist:
        if (util.mybasename(imgname) == 'Thumbs'):
            continue
        print('count: ', count)
        count = count + 1
        print(imgname)
        splitdata(imgname, args.gap, args.subsize)
        print('outlier1:', outlier1)
        print('outlier2:', outlier2)

if __name__ == '__main__':
    main()