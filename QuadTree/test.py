"""
Pygame script to test that the algorithm works.
"""
from math import sqrt
import sys

import numpy as np

import pygame
from pygame.locals import *

from quadtree import Point, Rect, QuadTree, centroid



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
	coords = np.random.randn(N, 2) * height/3 + (width/2, height/2)
	points = [Point(*coords[i], i) for i in range(len(coords))]

	domain = Rect(width/2, height/2, width, height)
	qtree = QuadTree(domain, 3)
	for point in points:
		qtree.insert(point)
		
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
		poly_mouse = makeCircleFromMouse()
		
		dist = list()
		collide = list()
  
		centre, radius = poly_mouse
		found_points = []
		qtree.query_radius(centre, radius, found_points)
		print(found_points)
		found_points = list(map(lambda x: x.payload , found_points))
			
		for i in range(len(coords)):
			polygon(makeBoxFormCenter(coords[i], 10, 10), GREEN if i in found_points else RED)
			
		circle(poly_mouse, BLUE)

		
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