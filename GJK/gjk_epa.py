from math import sqrt
import numpy as np
from numpy import add 
from numpy import subtract as sub
from numpy import negative as neg

def dot(v1, v2):
	return v1[0] * v2[0] + v1[1] * v2[1]

def normalize(vector):
	return vector / np.linalg.norm(vector)

def aXbXa(v1, v2):
	"""
	Performs v1 X v2 X v1 where X is the cross product. The
	input vectors are (x, y) and the cross products are
	performed in 3D with z=0. The output is the (x, y)
	component of the 3D cross product.
	"""
	x0 = v1[0]
	x1 = v1[1]
	x1y0 = x1 * v2[0]
	x0y1 = x0 * v2[1]
	return (x1 * (x1y0 - x0y1), x0 * (x0y1 - x1y0))

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
	if mag == 0: mag = 0.000001
	s = circle[1] / mag
	center = circle[0]
	return (center[0] + s * direction[0], center[1] + s * direction[1])

def support(poly1, poly2, support1, support2, direction):
	return sub(support1(poly1, direction), support2(poly2, neg(direction)))

def collidePolyPoly(poly1, poly2):
	return collide(poly1, poly2, supportPoly, supportPoly)

def collidePolyCircle(poly, circle):
	return collide(poly, circle, supportPoly, supportCircle)

def collideCircleCircle(poly, circle):
	return collide(poly, circle, supportCircle, supportCircle)

def collide(shape1, shape2, support1, support2):
	s = support(shape1, shape2, support1, support2, (-1, -1))
	simplex = [s]
	d = list(neg(s))

	for i in range(100):
		a = support(shape1, shape2, support1, support2, d)

		if dot(a, d) < 0:
			return False, ([(0,0),(0,0)], (0,0))

		simplex.append(a)

		if doSimplex(simplex, d):
			return True, epa(simplex, shape1, shape2, support1, support2)

	raise RuntimeError

def doSimplex(simplex, d):
	l = len(simplex)

	if l == 2:
		b = simplex[0]
		a = simplex[1]
		a0 = neg(a)
		ab = sub(b, a)

		if dot(ab, a0) >= 0:
			cross = aXbXa(ab, a0)
			d[0] = cross[0]
			d[1] = cross[1]
		else:
			simplex.pop(0)
			d[0] = a0[0]
			d[1] = a0[1]
	else:
		c = simplex[0]
		b = simplex[1]
		a = simplex[2]
		a0 = neg(a)
		ab = sub(b, a)
		ac = sub(c, a)

		if dot(ab, a0) >= 0:
			cross = aXbXa(ab, a0)

			if dot(ac, cross) >= 0:
				cross = aXbXa(ac, a0)

				if dot(ab, cross) >= 0:
					return True
				else:
					simplex.pop(1)
					d[0] = cross[0]
					d[1] = cross[1]
			else:
				simplex.pop(0)
				d[0] = cross[0]
				d[1] = cross[1]
		else:
			if dot(ac, a0) >= 0:
				cross = aXbXa(ac, a0)

				if dot(ab, cross) >= 0:
					return True
				else:
					simplex.pop(1)
					d[0] = cross[0]
					d[1] = cross[1]
			else:
				simplex.pop(1)
				simplex.pop(0)
				d[0] = a0[0]
				d[1] = a0[1]

	return False

def epa(polytope, shapeA, shapeB, f1 , f2):
	minIndex = 0
	minDistance = float('inf')
	# minNormal = 0

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
		else:
			break

	return minNormal * (minDistance + 0.001)

