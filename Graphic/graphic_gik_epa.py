frequency = 30
norm_noise = 0

from math import sqrt
import sys
import random as rd

import numpy as np

import pygame
from pygame.locals import *

from aabbtree import AABB, AABBTree
from GJK import gjk_epa
from distance_project import distance_poly_point, distance_circle_point, intersection_poly_poly, intersection_poly_circle, intersection_circle_circle


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)


class Display:
	height = 800
	width = 800
	
	SCREEN = pygame.display.set_mode((width, height))
	CLOCK = pygame.time.Clock()
 
	def __init__(self):
		pygame.init()
	
	@staticmethod
	def circles(cs, color=BLACK, camera=(0, 0)):
		for c in cs:
			Display.circle(c, color, camera)

	@staticmethod
	def circle(c, color=BLACK, camera=(0, 0)):
		pygame.draw.circle(Display.SCREEN, color, Display.add(c[0], camera), c[1])
	
	@staticmethod
	def pairs(points):
		for i, j in enumerate(range(-1, len(points) - 1)):
			yield (points[i], points[j])
	
	@staticmethod
	def polygon(points, color=BLACK, camera=(0, 0)):
		for a, b in Display.pairs(points):
			Display.line(a, b, color, camera)

	@staticmethod
	def line(start, end, color=BLACK, camera=(0, 0)):
		pygame.draw.line(Display.SCREEN, color, Display.add(start, camera), Display.add(end, camera))

	@staticmethod
	def add(p1, p2):
		return p1[0] + p2[0], p1[1] + p2[1]

	@staticmethod
	def printText(text, pos):
		f1 = pygame.font.Font(None, 36)
		text1 = f1.render(text, 1, (180, 0, 0))
		Display.SCREEN.blit(text1, pos)

	@staticmethod
	def log(obj, dist, angl):
		print(obj, dist, angl)
    
	
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

	def makeFromMouse(poly):
		pos = pygame.mouse.get_pos()
		return tuple(map(lambda x: (x[0] + pos[0], x[1] + pos[1], poly)))

	def makeBoxFromMouse(w, h):
		pos = pygame.mouse.get_pos()

		return (
			( w + pos[0],  h + pos[1]),
			( w + pos[0], -h + pos[1]),
			( -w + pos[0], -h + pos[1]),
			( -w + pos[0], h + pos[1])
		)
  
	def getMinMax(self): return self.minMaxXY
 
	def collide(self, obj):
		return obj.collidePoly(self.poly)

	def collideCircle(self, circle):
		return gjk_epa.collidePolyCircle(self.poly, circle)

	def collidePoly(self, poly):
		return gjk_epa.collidePolyPoly(self.poly, poly)

	def draw(self, color):
		Display.polygon(self.poly, color)
  
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
		return intersection_poly_circle(poly1.poly, self)
		# return []
	
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

	def makeFromMouse(R):
		noise = rd.randint(-norm_noise, norm_noise)
		return Circle(tuple(map(lambda x: x +  noise, pygame.mouse.get_pos())), R)	 

	def getMinMax(self): return self.minMaxXY
	
	def draw(self, color):
		Display.circle(self.getCircle(), color)
  
	def getCircle(self):
		return (self.center, self.radius)

	def collide(self, obj):
		return obj.collideCircle(self.getCircle())

	def collideCircle(self, circle):
		return gjk_epa.collideCircleCircle(self.getCircle(), circle)

	def collidePoly(self, poly):
		return gjk_epa.collidePolyCircle(poly, self.getCircle())

	def dictance_to_point(self,point):
		return distance_circle_point(point,self)

	def intersection(self, obj):
		return obj.intersection_circle(self)

	def intersection_poly(self,poly1):
		# return intersection_poly_circle(poly1.poly, self)
		return []

	def intersection_circle(self,circle1):
		return intersection_circle_circle(self, circle1)