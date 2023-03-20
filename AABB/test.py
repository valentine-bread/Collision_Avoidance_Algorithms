from math import sqrt
import sys

import numpy as np

import pygame
from pygame.locals import *

from aabbtree import AABB, AABBTree
# tree = AABBTree()
# aabb1 = AABB([(0, 0), (0, 0)])
# aabb2 = AABB([(-1, 1), (-1, 1)])
# aabb3 = AABB([(4, 5), (2, 3)])
# tree.add(aabb1, 'box 1')
# tree.does_overlap(aabb2)
# tree.overlap_values(aabb2)
# tree.does_overlap(aabb3)
# tree.add(aabb3)
# print(tree)




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
	N = 20
	allobj = [makeBoxFormCenter(coord, 10, 10) for coord in np.random.randn(N, 2) * height/3 + (width/2, height/2)]
	tree = AABBTree()
	for i in range(len(allobj)):
		aabb = AABB(get_min_max_poly(allobj[i]))
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
		poly_mouse = makeBoxFromMouse()
  
		aabb = AABB(get_min_max_poly(poly_mouse))
		found_points = tree.overlap_values(aabb)
			
		for i in range(len(allobj)):
			polygon(allobj[i], GREEN if i in found_points else RED)
			
		polygon(poly_mouse, BLUE)

		
		pygame.display.flip()
		CLOCK.tick(60)

def makeCircleFromMouse():
	pos = pygame.mouse.get_pos()

	return (
		((0 + pos[0], 0 + pos[1]), 60)
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

def get_min_max_poly(poly):
    X = list(map(lambda x: x[0], poly)) 
    Y = list(map(lambda x: x[1], poly)) 
    return [(min(X), max(X)), (min(Y), max(Y))]
	

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