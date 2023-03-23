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

def run():
	
	wall = [(
		(0, 0),	(0, 150), (10, 150), (10, 0)),
		((0, 150), (0, 550), (10, 550), (10, 150)),
  
		((0, 150), (0, 550), (10, 550),	(10, 150)),
		((10, 0), (10, 10), (380, 10), (380, 0)),
  
		((380, 0), (380, 10), (580, 10), (580, 0)),
    	((570, 10), (580, 10), (580, 550), (570, 550)),
     
     	((0, 550), (0, 560), (380, 560), (380, 550)),
		((380, 550), (380, 560), (580, 560), (580, 550)),
  
  		((380, 550), (380, 10), (390, 10), (390, 550)),
    
    	((10, 150), (10, 160), (390, 160), (390, 150))]

	
	allpoly, allcircle = list(), list()
	# for poly in wall: allpoly.append(poly)	
	allpoly += wall
	# for circleObj in allcircle: allpoly.append(circle)
	
	
	# N = 20
	# allobj = [makeBoxFormCenter(coord, 10, 10) for coord in np.random.randn(N, 2) * height/3 + (width/2, height/2)]
	tree = AABBTree()
	for i in range(len(allpoly)):
		aabb = AABB(getMinMaxPoly(allpoly[i]))
		tree.add(aabb, i)   
	for i in range(len(allcircle)):
		aabb = AABB(getMinMaxCircle(allcircle[i]))
		tree.add(aabb) 


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
		poly_mouse = makeCircleFromMouse(20)
  
		# for i in range(len(allobj)):
		# 	polygon(allobj[i], RED)
  
		aabb = AABB(getMinMaxCircle(poly_mouse))
		found_points = tree.overlap_values(aabb)
  
		dist = list()
		collide = list()	
			
		for i in range(len(allpoly)):
			polygon(allpoly[i], BLACK)
			if i in found_points:
				col, d = gjk_epa.collidePolyCircle(allpoly[i], poly_mouse)
				dist.append(d)
				collide.append(col)
    	
		if found_points:
			d_max = list(map(lambda x: sqrt(x[0] ** 2 + x[1] ** 2), dist))
			index = d_max.index(max(d_max))
			print(d_max[index])
			line((200,200), (dist[index][0] + 200, dist[index][1] + 200))
			circle(poly_mouse, GREEN)
		else:
			circle(poly_mouse, RED)
   
			
		# polygon(poly_mouse, BLUE)
		
		pygame.display.flip()
		CLOCK.tick(60)

def makeCircleFromMouse(R):
	pos = pygame.mouse.get_pos()

	return (
		((0 + pos[0], 0 + pos[1]), R)
	)

def makePolyFromMouse():
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
	
def makeBoxFormCenter(center, h, w):
	return (
		( center[0] + h, center[1] + w),
		( center[0] + h, center[1] - w),
		( center[0] - h, center[1] - w),
		( center[0] - h, center[1] + w)
	)

def getMinMaxPoly(poly):
	X = list(map(lambda x: x[0], poly)) 
	Y = list(map(lambda x: x[1], poly)) 
	return [(min(X), max(X)), (min(Y), max(Y))]
	
def getMinMaxCircle(XY):
    return [(XY[0][0] - XY[1], XY[0][0] + XY[1]), (XY[0][1] - XY[1], XY[0][1] + XY[1])]

def pairs(points):
	for i, j in enumerate(range(-1, len(points) - 1)):
		yield (points[i], points[j])

def circles(cs, color=BLACK, camera=(0, 0)):
	for c in cs:
		circle(c, color, camera)

def circle(c, color=BLACK, camera=(0, 0)):
	pygame.draw.circle(SCREEN, color, add(c[0], camera), c[1])

def polygon(points, color=BLACK, camera=(0, 0)):
	for a, b in pairs(points):
		line(a, b, color, camera)

def line(start, end, color=BLACK, camera=(0, 0)):
	pygame.draw.line(SCREEN, color, add(start, camera), add(end, camera))

def add(p1, p2):
	return p1[0] + p2[0], p1[1] + p2[1]

if __name__ == '__main__':
	run()	