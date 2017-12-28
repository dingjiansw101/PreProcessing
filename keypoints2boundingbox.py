import os
import utils as util
import shapely.geometry as shgeo
import numpy as np
import codecs

def plane_keypoints2bbx(points):
    p1 = (points[0], points[1])
    p2 = (points[2], points[3])
    p3 = (points[4], points[5])
    p4 = (points[6], points[7])
    line1 = shgeo.LineString((p1, p3))
    line2 = shgeo.LineString((p2, p4))
    intersection = line1.intersection(line2)
    vec1 = np.array(p1) - np.array(intersection)
    print('vec1:', vec1)
    vec2 = np.array(p3) - np.array(intersection)
    outp1 = p4 + vec1
    outp2 = p2 + vec1
    outp3 = p2 + vec2
    outp4 = p4 + vec2
    bbx = (outp1[0], outp1[1],
           outp2[0], outp2[1],
           outp3[0], outp3[1],
           outp4[0], outp4[1])
    print('intersection:', intersection)
    return bbx
def plane_keypoints2horizonbbx(points):
    p1 = (points[0], points[1])
    p2 = (points[2], points[3])
    p3 = (points[4], points[5])
    p4 = (points[6], points[7])
    xmin = min(p1[0], min(p2[0], min(p3[0], p4[0])))
    ymin = min(p1[1], min(p2[1], min(p3[1], p4[1])))
    xmax = max(p1[0], max(p2[0], max(p3[0], p4[0])))
    ymax = max(p1[1], max(p2[1], max(p3[1], p4[1])))
    bbx = (xmin, ymin,
           xmax, ymin,
           xmax, ymax,
           xmin, ymax)
    return bbx
def test():
    points = [665, 2191, 723, 1955, 910, 2000, 903, 2189]
    plane_keypoints2bbx(points)

def main():
    srcfile = r'E:\GoogleEarth\alibaba\bbox\jinpu_22.txt'
    dstfile = r'E:\GoogleEarth\alibaba\horizontbbx\jinpu_22.txt'
    with codecs.open(dstfile, 'w', 'utf_16') as f_out:
        with codecs.open(srcfile, 'r', 'utf_16') as f:
            objects = util.parse_bod_poly2(srcfile)
            for obj in objects:
                keypoints = obj['poly']
                #bbx = plane_keypoints2bbx(keypoints)
                bbx = plane_keypoints2horizonbbx(keypoints)
                outline = ' '.join(map(str, bbx)) + ' ' + '0A'
                f_out.write(outline + '\n')
if __name__ == '__main__':
    main()
    #test()