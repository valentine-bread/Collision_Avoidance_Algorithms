from math import sqrt, sin, cos, atan2
import numpy as np
from shapely.geometry import Polygon, Point

distance_point_point = lambda point1, point2: sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)


def distance(vector):
	return sqrt(vector[0] ** 2 + vector[1] ** 2)

# def epa_plus(polytope, shapeA, shapeB, f1 , f2):
#     normal = epa(polytope, shapeA, shapeB, f1 , f2)
#     shapeB = list(map(lambda x: (x[0] + normal[0], x[1] + normal[1]), shapeB))
    
    
def normalize(vector):
	return vector / np.linalg.norm(vector) 

def angle(v1, v2 = [(1,0),(0,0)], deg = True):
	v1_u = normalize(v1)
	v2_u = normalize(v2)
	radians = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
	result = radians
	if deg:
		result = np.degrees([radians.real])[0]  # переводим в градусы
 
	return result

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
    dictance = distance_point_point(point, circle.center) - circle.radius 
    if dictance <= circle.radius: distance = 0
    # d = sqrt((x1 - x2)**2 + (y1 - y2)**2)
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


def intersection_poly_circle(poly, circle):
    poly = Polygon(poly)
    circle = Point(circle.center).buffer(circle.radius)

    intersections = poly.exterior.intersection(circle)
    if intersections.is_empty:
        return ()
    elif intersections.geom_type.startswith('Multi') or intersections.geom_type == 'GeometryCollection':
        intersections.explode() 
        for f in intersections:
            return f.coords
    else:
        return intersections.coords.xy

    
    
def intersection_circle_circle(circle1, circle2):
    (x0, y0), r0 = circle1.center, circle1.radius 
    (x1, y1), r1 = circle2.center, circle2.radius 

    d=sqrt((x1-x0)**2 + (y1-y0)**2)
    if d > r0 + r1 :
        return []
    if d < abs(r0-r1):
        return []
    if d == 0 and r0 == r1:
        return []
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d   
        return [(x3, y3), (x4, y4)]
    
    
    
# from shapely.geometry import Polygon, Point, LinearRing  
# # задаем координаты вершин полигона 
# polygon_coords = [(0, 0), (0, 5), (5, 5), (5, 0)]  
# # создаем объект полигона 
# polygon = Polygon(polygon_coords)  # задаем центр окружности и ее радиус 
# circle_center = Point(2.5, 2.5) 
# circle_radius = 10  
# # находим точки пересечения полигона и окружности 
# circle = Point(0.5, 0.5).buffer(0.5)
# intersection = polygon.intersection(circle)
# # выводим координаты точек пересечения 
# pts = list(intersection.exterior.coords)
# print(pts)
# xx, yy = intersection_points.exterior.coords.xy
# # print(xx.tolist(), yy.tolist()) 
# print(list(zip(xx.tolist(), yy.tolist())))
