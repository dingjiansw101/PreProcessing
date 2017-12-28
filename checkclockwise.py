import utils as util


def validate_clockwise_points(points):
    """
    Validates that the points that the 4 points that dlimite a polygon are in clockwise order.
    """

    if len(points) != 8:
        raise Exception("Points list not valid." + str(len(points)))

    point = [
        [int(points[0]), int(points[1])],
        [int(points[2]), int(points[3])],
        [int(points[4]), int(points[5])],
        [int(points[6]), int(points[7])]
    ]
    edge = [
        (point[1][0] - point[0][0]) * (point[1][1] + point[0][1]),
        (point[2][0] - point[1][0]) * (point[2][1] + point[1][1]),
        (point[3][0] - point[2][0]) * (point[3][1] + point[2][1]),
        (point[0][0] - point[3][0]) * (point[0][1] + point[3][1])
    ]

    summatory = edge[0] + edge[1] + edge[2] + edge[3];
    if summatory > 0:
        return False
    else:
        return True

def getallbodobjects():
    filelist = util.GetFileFromThisRootDir(r'E:\bod-dataset\datadebug2\datadebug\labelTxt')
    allobjects = []
    for fullname in filelist:
        objects = util.parse_bod_poly2(fullname)
        allobjects = allobjects + objects
    return allobjects

def test():
    allobjects = getallbodobjects()
    total = 0
    for obj in allobjects:
        #print(obj)
        #if (obj['name'] not in util.noorientationnames) and (obj['name'] == 'baseball-diamond'):
        check  = validate_clockwise_points(obj['poly'])
        if not check:
            total= total+ 1
    print(total)
if __name__ == '__main__':
    test()