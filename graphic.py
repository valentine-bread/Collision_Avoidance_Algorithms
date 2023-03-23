from math import sqrt
import sys

import numpy as np

import pygame
from pygame.locals import *

from aabbtree import AABB, AABBTree
from GJK import gjk_epa
 
pygame.init()
height = 600
width = 800
SCREEN = pygame.display.set_mode((width, height))
CLOCK = pygame.time.Clock()

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

	def makeFromMouse():
		pos = pygame.mouse.get_pos()
		return (
			( 50 + pos[0],  50 + pos[1]),
			( 50 + pos[0], -15 + pos[1]),
			( 40 + pos[0], -30 + pos[1]),
			( 20 + pos[0], -50 + pos[1]),
			(  0 + pos[0], -50 + pos[1]),
			(-60 + pos[0],   0 + pos[1])
		)

	def makeBoxFromMouse():
		pos = pygame.mouse.get_pos()

		return (
			( 50 + pos[0],  50 + pos[1]),
			( 50 + pos[0], -15 + pos[1]),
			( -15 + pos[0], -15 + pos[1]),
			( -15 + pos[0], 50 + pos[1])
		)
  
	def getMinMax(self): return self.minMaxXY
 
	def collide(self, obj):
		return obj.collidePoly(self.poly)

	def collideCircle(self, circle):
		return gjk_epa.collidePolyCircle(self.poly, circle)

	def collidePoly(self, poly):
		return gjk_epa.collidePolyCircle(self.poly, poly)

	def draw(self, color):
		polygon(self.poly, color)
  
	def getPoly(self):
		return self.poly
	
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
		return Circle(pygame.mouse.get_pos(), R)	 

	def getMinMax(self): return self.minMaxXY
	
	def draw(self, color):
		circle(self.getCircle(), color)
  
	def getCircle(self):
		return (self.center, self.radius)

	def collide(self, obj):
		return obj.collideCircle(self.getCircle())

	def collideCircle(self, circle):
		return gjk_epa.collideCircleCircle(self.getCircle(), circle)

	def collidePoly(self, poly):
		return gjk_epa.collidePolyCircle(poly, self.getCircle())




def run():
	
	wall = [
    	Poly([(0, 0), (0, 150), (10, 150), (10, 0)]),
		Poly([(0, 150), (0, 550), (10, 550), (10, 150)]),
  
		Poly([(0, 150), (0, 550), (10, 550),	(10, 150)]),
		Poly([(10, 0), (10, 10), (380, 10), (380, 0)]),
  
		Poly([(380, 0), (380, 10), (580, 10), (580, 0)]),
    	Poly([(570, 10), (580, 10), (580, 550), (570, 550)]),
     
     	Poly([(0, 550), (0, 560), (380, 560), (380, 550)]),
		Poly([(380, 550), (380, 560), (580, 560), (580, 550)]),
  
  		Poly([(380, 550), (380, 10), (390, 10), (390, 550)]),
    
    	Poly([(10, 150), (10, 160), (390, 160), (390, 150)]),
     	
      	Circle((100,100),40)]

	
	allobj = list()
	allobj += wall
	# N = 20
	# allobj = [makeBoxFormCenter(coord, 10, 10) for coord in np.random.randn(N, 2) * height/3 + (width/2, height/2)]
	tree = AABBTree()
	for i in range(len(allobj)):
		aabb = AABB(allobj[i].getMinMax())
		tree.add(aabb, i)   


	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()
				elif event.key == K_UP:
					pass
				elif event.key == K_DOWN:
					pass
				elif event.key == K_LEFT:
					pass
				elif event.key == K_RIGHT:
					pass
				

		SCREEN.fill(WHITE)
		poly_mouse = Circle.makeFromMouse(20)
		aabb = AABB(poly_mouse.getMinMax())
		found_points = tree.overlap_values(aabb)
  
		dist = list()
		collide = list()	
			
		for i in range(len(allobj)):
			allobj[i].draw(BLACK)
			if i in found_points:
				col, d = allobj[i].collide(poly_mouse)
				dist.append(d)
				collide.append(col)
    	
		if found_points:
			d_max = list(map(lambda x: sqrt(x[0] ** 2 + x[1] ** 2), dist))
			index = d_max.index(max(d_max))
			print(d_max[index])
			line((200,200), (dist[index][0] + 200, dist[index][1] + 200))
			poly_mouse.draw(GREEN)
		else:
			poly_mouse.draw(RED)
   
			
		
		pygame.display.flip()
		CLOCK.tick(60)



def circles(cs, color=BLACK, camera=(0, 0)):
	for c in cs:
		circle(c, color, camera)

def circle(c, color=BLACK, camera=(0, 0)):
	pygame.draw.circle(SCREEN, color, add(c[0], camera), c[1])
 
def pairs(points):
	for i, j in enumerate(range(-1, len(points) - 1)):
		yield (points[i], points[j])


def polygon(points, color=BLACK, camera=(0, 0)):
	for a, b in pairs(points):
		line(a, b, color, camera)

def line(start, end, color=BLACK, camera=(0, 0)):
	pygame.draw.line(SCREEN, color, add(start, camera), add(end, camera))

def add(p1, p2):
	return p1[0] + p2[0], p1[1] + p2[1]

if __name__ == '__main__':
	run()	