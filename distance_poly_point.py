from math import sqrt
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
    if check_point_in_poly(point, poly) == 1: return 0
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
    
    
    

 

# def distance_point_to_line(point, line):
#     x0, y0 = point
#     x1, y1 = line[0]
#     x2, y2 = line[1]
#     numerator = abs((y2-y1)*x0 - (x2-x1)*y0 + x2*y1 - y2*x1)
#     denominator = ((y2-y1)**2 + (x2-x1)**2)**0.5
#     distance = numerator / denominator
#     return distance

# def project_point_on_vector(point, vector): 
#     point = np.array(point)
#     vector = np.array(vector)
#     return (np.dot(point, vector) / np.dot(vector, vector) * vector).tolist()


# print(distance_point_point((100,100),(300,300)))
# print(distance_poly_point((300, 300), ((-100,100),(100,100),(100,-100),(-100,-100))))

# point = (1, 1) 
# segment = ((0, 0), (4, 4))  
# projected_point = project_point_to_segment(point, segment) 
# print(projected_point) 