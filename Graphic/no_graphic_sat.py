frequency = 30
norm_noise = 0

from math import sqrt
import sys
import random as rd

import numpy as np

from aabbtree import AABB, AABBTree
from SAT import sat
from distance_project import distance_poly_point, distance_circle_point, intersection_poly_poly, intersection_poly_circle, intersection_circle_circle


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

	
class Poly():
	poly = list()
	minMaxXY = 0
		
	def __init__(self, poly):
		self.poly = poly
		self.minMaxXY = self.minMax()
	
	def minMax(self):
		X = list(map(lambda x: x[0], self.poly)) 
		Y = list(map(lambda x: x[1], self.poly)) 
		return [(min(X), max(X)), (min(Y), max(Y))]
  
	def getMinMax(self): return self.minMaxXY
 
	def collide(self, obj):
		return obj.collidePoly(self.poly)

	def collideCircle(self, circle):
		return sat.separating_axis_theorem(self.poly, circle)

	def collidePoly(self, poly):
		return sat.separating_axis_theorem(self.poly, poly)
  
	def getPoly(self):
		return self.poly

	def add(self, cx, cy):
		self.poly = list(map(lambda x: (x[0] + cx, x[1] + cy), self.poly))
		self.minMaxXY = self.minMax()
  
	def __len__(self):
		return len(self.poly)

	def intersection(self, obj):
		return obj.intersection_poly(self)

	def dictance_to_point(self,point):
		return distance_poly_point(point,self.poly)

	def intersection_poly(self,poly1):
		return intersection_poly_poly(self.poly, poly1.poly)

	def intersection_circle(self,poly1):
		# return intersection_poly_circle(poly1.poly, self)
		return []
	
class Circle():
	center = (0,0)
	radius = 0
	minMaxXY = 0

	def __init__(self, center, radius):
		self.center = center
		self.radius = radius
		self.minMaxXY = self.minMax()

	def minMax(self):
		return [(self.center[0] - self.radius, self.center[0] + self.radius), (self.center[1] - self.radius, self.center[1] + self.radius)]


	def getMinMax(self): return self.minMaxXY
	
  
	def getCircle(self):
		return (self.center, self.radius)

	def collide(self, obj):
		return obj.collideCircle(self.getCircle())

	def collideCircle(self, circle):
		return sat.separating_axis_theorem(self.getCircle(), circle)

	def collidePoly(self, poly):
		return sat.separating_axis_theorem(poly, self.getCircle())

	def dictance_to_point(self,point):
		return distance_circle_point(point,self)

	def intersection(self, obj):
		return obj.intersection_circle(self)

	def intersection_poly(self,poly1):
		# return intersection_poly_circle(poly1.poly, self)
		return []

	def intersection_circle(self,circle1):
		return intersection_circle_circle(self, circle1)