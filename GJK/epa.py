from math import sqrt
import numpy as np

def sub(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def neg(v):
    return (-v[0], -v[1])

def supportPoly(polygon, direction):
    bestPoint = polygon[0]
    bestDot = dot(bestPoint, direction)

    for i in range(1, len(polygon)):
        p = polygon[i]
        d = dot(p, direction)

        if d > bestDot:
            bestDot = d
            bestPoint = p

    return bestPoint

def supportCircle(circle, direction):
    mag = sqrt(dot(direction, direction))
    s = circle[1] / mag
    center = circle[0]
    return (center[0] + s * direction[0], center[1] + s * direction[1])

def support(poly1, poly2, support1, support2, direction):
    return sub(support1(poly1, direction), support2(poly2, neg(direction)))

def normalize(vector):
    if vector == (0,0): return vector
    norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector[0] / norm, vector[1] / norm


def epa_PolyPoly(polytope, shapeA, shapeB):
    return epa(polytope, shapeA, shapeB, supportPoly , supportPoly)

def epa_PolyCircle(polytope, shapeA, shapeB):
    return epa(polytope, shapeA, shapeB, supportPoly , supportCircle)

def epa(polytope, shapeA, shapeB, f1 , f2):
	minIndex = 0
	minDistance = float('inf')
	minNormal = 0

	while (minDistance == float('inf')): 
		for i in range(0, len(polytope)): 
			j = (i+1) % len(polytope)
			vertexI = polytope[i]
			vertexJ = polytope[j]
			ij = sub(vertexJ, vertexI)

			normal = np.array(normalize((ij[1], -ij[0])))
			distance = dot(normal,vertexI)

			if (distance < 0):
				distance *= -1
				normal *= -1
			

			if (distance < minDistance):
				minDistance = distance
				minNormal = normal
				minIndex = j
    
		support_t = support(shapeA, shapeB, f1, f2, minNormal)
		sDistance = dot(minNormal,support_t)

		if(abs(sDistance - minDistance) > 0.001):
			minDistance = float('inf')
			polytope.insert(minIndex, support_t)

	return minNormal * (minDistance + 0.001)

		