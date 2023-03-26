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


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)


class Display:
	height = 600
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


# def run():
	
# 	wall = [
# 		Poly([(0, 0), (0, 150), (10, 150), (10, 0)]),
# 		Poly([(0, 150), (0, 550), (10, 550), (10, 150)]),
  
# 		Poly([(0, 150), (0, 550), (10, 550),	(10, 150)]),
# 		Poly([(10, 0), (10, 10), (380, 10), (380, 0)]),
  
# 		Poly([(380, 0), (380, 10), (580, 10), (580, 0)]),
# 		Poly([(570, 10), (580, 10), (580, 550), (570, 550)]),
	 
# 	 	Poly([(0, 550), (0, 560), (380, 560), (380, 550)]),
# 		Poly([(380, 550), (380, 560), (580, 560), (580, 550)]),
  
#   		Poly([(380, 550), (380, 10), (390, 10), (390, 550)]),
	
# 		Poly([(10, 150), (10, 160), (390, 160), (390, 150)])
# 	]
# 	list(map(lambda x: x.add(50, 50), wall))
	 
# 	furniture = [
# 		Circle((100,100),40)
# 	]
	  	

	
# 	allobj = list(wall)
# 	allobj += furniture
	
# 	# N = 20
# 	# allobj = [makeBoxFormCenter(coord, 10, 10) for coord in np.random.randn(N, 2) * height/3 + (width/2, height/2)]
# 	tree = AABBTree()
# 	for i in range(len(allobj)):
# 		aabb = AABB(allobj[i].getMinMax())
# 		tree.add(aabb, i)   


# 	while True:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				sys.exit()
# 			elif event.type == KEYDOWN:
# 				if event.key == K_ESCAPE:
# 					sys.exit()
# 				elif event.key == K_UP:
# 					pass
# 				elif event.key == K_DOWN:
# 					pass
# 				elif event.key == K_LEFT:
# 					pass
# 				elif event.key == K_RIGHT:
# 					pass
				

# 		SCREEN.fill(WHITE)
# 		poly_mouse = Circle.makeFromMouse(20)
# 		aabb = AABB(poly_mouse.getMinMax())
# 		found_points = tree.overlap_values(aabb)
  
# 		# dist = list()
# 		result = list()
# 		collide = False	
			
# 		for i in range(len(allobj)):
# 			allobj[i].draw(BLACK)
# 			if i in found_points:
# 				col, vector = allobj[i].collide(poly_mouse)
# 				if col:
# 					result.append((i, gjk_epa.dist(vector), gjk_epa.angle(vector)))
# 					# dist.append(d)
# 					collide = True
		
# 		if collide:
# 			for r in result:
# 				log(*r)
# 			# d_max = list(map(gjk_epa.dist, dist))
# 			# index = d_max.index(max(d_max))
# 			# # print(d_max[index], gjk_epa.angle(dist[index]))
# 			# printText(str(int(d_max[index])), (0,0))
# 			# printText(str(int(gjk_epa.angle(dist[index]))), (0,20))
# 			# line((200,200), (dist[index][0] + 200, dist[index][1] + 200))
# 			poly_mouse.draw(GREEN)
# 		else:
# 			poly_mouse.draw(RED)
   
# 		pygame.display.flip()
# 		CLOCK.tick(frequency)



# def circles(cs, color=BLACK, camera=(0, 0)):
# 	for c in cs:
# 		circle(c, color, camera)

# def circle(c, color=BLACK, camera=(0, 0)):
# 	pygame.draw.circle(SCREEN, color, add(c[0], camera), c[1])
 
# def pairs(points):
# 	for i, j in enumerate(range(-1, len(points) - 1)):
# 		yield (points[i], points[j])


# def polygon(points, color=BLACK, camera=(0, 0)):
# 	for a, b in pairs(points):
# 		line(a, b, color, camera)

# def line(start, end, color=BLACK, camera=(0, 0)):
# 	pygame.draw.line(SCREEN, color, add(start, camera), add(end, camera))

# def add(p1, p2):
# 	return p1[0] + p2[0], p1[1] + p2[1]

# def printText(text, pos):
# 	f1 = pygame.font.Font(None, 36)
# 	text1 = f1.render(text, 1, (180, 0, 0))
# 	SCREEN.blit(text1, pos)

# def log(obj, dist, angl):
#     print(obj, dist, angl)

# if __name__ == '__main__':
# 	run()	
 
