import numpy as np
import shapely
from shapely.geometry import Polygon, MultiPoint

def polygon_from_list(line):
    """
    Create a shapely polygon object from gt or dt line.
    """
    # polygon_points = [float(o) for o in line.split(',')[:8]]
    polygon_points = np.array(line).reshape(4, 2)
    polygon = Polygon(polygon_points).convex_hull
    return polygon


def polygon_iou(list1, list2):
    """
    Intersection over union between two shapely polygons.
    """
    polygon_points1 = np.array(list1).reshape(4, 2)
    poly1 = Polygon(polygon_points1).convex_hull
    polygon_points2 = np.array(list2).reshape(4, 2)
    poly2 = Polygon(polygon_points2).convex_hull
    union_poly = np.concatenate((polygon_points1, polygon_points2))
    if not poly1.intersects(poly2):  # this test is fast and can accelerate calculation
        iou = 0
    else:
        try:
            inter_area = poly1.intersection(poly2).area
            # union_area = poly1.area + poly2.area - inter_area
            union_area = MultiPoint(union_poly).convex_hull.area
            if union_area == 0:
                return 0
            iou = float(inter_area) / union_area
        except shapely.geos.TopologicalError:
            print('shapely.geos.TopologicalError occured, iou set to 0')
            iou = 0
    return iou


def nms(boxes, overlap):
    if len(boxes[0]) == 9:
        score_pos = 8
    elif len(boxes[0]) == 10:
        score_pos = 9
    else:
        print("wrong boxes shape!")
        return
    rec_scores = [b[score_pos] for b in boxes]
    indices = sorted(range(len(rec_scores)), key=lambda k: -rec_scores[k])
    box_num = len(boxes)
    nms_flag = [True] * box_num
    for i in range(box_num):
        ii = indices[i]
        print('i:', i)
        if not nms_flag[ii]:
            continue
        for j in range(box_num):
            jj = indices[j]
            if j == i:
                continue
            if not nms_flag[jj]:
                continue
            box1 = boxes[ii]
            box2 = boxes[jj]
            box1_score = rec_scores[ii]
            box2_score = rec_scores[jj]
            # str1 = box1[9]
            # str2 = box2[9]
            # box_i = [box1[0], box1[1], box1[4], box1[5]]
            # box_j = [box2[0], box2[1], box2[4], box2[5]]
            poly1 = polygon_from_list(box1[0:8])
            poly2 = polygon_from_list(box2[0:8])
            iou = polygon_iou(box1[0:8], box2[0:8])
            thresh = overlap

            if iou > thresh:
                if box1_score > box2_score:
                    nms_flag[jj] = False
                if box1_score == box2_score and poly1.area > poly2.area:
                    nms_flag[jj] = False
                if box1_score == box2_score and poly1.area <= poly2.area:
                    nms_flag[ii] = False
                    break
            '''
            if abs((box_i[3]-box_i[1])-(box_j[3]-box_j[1]))<((box_i[3]-box_i[1])+(box_j[3]-box_j[1]))/2:
                if abs(box_i[3]-box_j[3])+abs(box_i[1]-box_j[1])<(max(box_i[3],box_j[3])-min(box_i[1],box_j[1]))/3:
                    if box_i[0]<=box_j[0] and (box_i[2]+min(box_i[3]-box_i[1],box_j[3]-box_j[1])>=box_j[2]):
                        nms_flag[jj] = False
            '''
    return nms_flag