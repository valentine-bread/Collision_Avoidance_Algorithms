from math import sqrt, sin, cos, atan2
import numpy as np

distance_point_point = lambda point1, point2: sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def project_point_to_segment(point, segment):     
    """     
    Возвращает проекцию точки на отрезок в координатах.          
    :param point: кортеж (x, y) с координатами точки     
    :param segment: кортеж ((x1, y1), (x2, y2)) с координатами концов отрезка     
    :return: кортеж (x, y) с координатами проекции точки на отрезок     
    """     
    x, y = point     
    (x1, y1), (x2, y2) = segment      
    dx, dy = x2 - x1, y2 - y1     
    dot_product = (x - x1) * dx + (y - y1) * dy     
    segment_length_squared = dx * dx + dy * dy      
    if segment_length_squared == 0:         
        return x1, y1     
    normalized_distance = max(0, min(1, dot_product / segment_length_squared))     
    x_proj, y_proj = x1 + normalized_distance * dx, y1 + normalized_distance * dy      
    return x_proj, y_proj 

def check_point_in_poly(point, poly):
    c=0
    xp = list(map(lambda x: x[0], poly))
    yp = list(map(lambda x: x[1], poly))
    x,y = point[0], point[1],
    for i in range(len(xp)):
        if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and 
            (x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c    
    return c
    
def distance_poly_point(point, poly):
    min_distance = 0
    for i in range(len(poly)):
        tmp_distance = distance_point_point(poly[i], point)
        if min_distance > tmp_distance:
            min_point, min_distance = i, tmp_distance
    if check_point_in_poly(point, poly) == 1: 
        return 0, point
    edges = [(poly[i],poly[i+1]) for i in range(len(poly)-1)]
    edges.append((poly[0], poly[len(poly)-1])) 
    min_dist = float('inf')
    min_project = point
    for edge in edges:
        project = project_point_to_segment(point, edge)
        dist = distance_point_point(point, project)
        if min_dist > dist:
            min_dist, min_project = dist, project
    return (min_dist, min_project)

def distance_circle_point(point, circle):
    r = circle.radius
    x1, y1 = point
    x2, y2 = circle.center
    dictance = circle.radius - distance_point_point(point, circle.center)
    d = sqrt((x1 - x2)**2 + (y1 - y2)**2)
    angle = atan2(y1 - y2, x1 - x2)
    x_proj = x2 + r * cos(angle)
    y_proj = y2 + r * sin(angle)
    return dictance, (x_proj, y_proj)
    

def intersection_libe_line(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None
    
    def onSegment(p, q, r):
        if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    if onSegment(line1[0],(x,y),line1[1]) and onSegment(line2[0],(x,y),line2[1]):
        return x, y

def intersection_poly_poly(polygon1, polygon2):
    intersections = []
    for i in range(len(polygon1)):
        line1 = [polygon1[i-1], polygon1[i]]
        for j in range(len(polygon2)):
            line2 = [polygon2[j-1], polygon2[j]]
            point = intersection_libe_line(line1, line2)
            if point is not None:
                intersections.append(point)
    return intersections


polygon1 = [(0, 0), (4, 0), (4, 4), (0, 4)]
polygon2 = [(2, 2), (6, 2), (6, 6), (2, 6)]

# выведем список точек пересечения
intersections = intersection_poly_poly(polygon1, polygon2)
print("Точки пересечения: ", intersections)
print(intersection_libe_line([(0, 0),(0, 4)], [(2, 2),(6, 2)]))