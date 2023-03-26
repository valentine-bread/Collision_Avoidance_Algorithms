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

from Graphic.graphic_gik_epa import Display, Poly, Circle, BLACK, WHITE, BLUE, GREEN, RED


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
	
		Poly([(10, 150), (10, 160), (390, 160), (390, 150)])
	]
	list(map(lambda x: x.add(50, 50), wall))
	 
	furniture = [
		Circle((100,100),40)
	]
	  	

	
	allobj = list(wall)
	allobj += furniture
	
	# N = 20
	# allobj = [makeBoxFormCenter(coord, 10, 10) for coord in np.random.randn(N, 2) * height/3 + (width/2, height/2)]
	tree = AABBTree()
	for i in range(len(allobj)):
		aabb = AABB(allobj[i].getMinMax())
		tree.add(aabb, i)   

	display = Display()

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
				

		display.SCREEN.fill(WHITE)
		poly_mouse = Circle.makeFromMouse(20)
		aabb = AABB(poly_mouse.getMinMax())
		found_points = tree.overlap_values(aabb)
  
		# dist = list()
		result = list()
		collide = False	
			
		for i in range(len(allobj)):
			allobj[i].draw(BLACK)
			if i in found_points:
				col, vector = allobj[i].collide(poly_mouse)
				if col:
					result.append((i, gjk_epa.dist(vector), gjk_epa.angle(vector)))
					display.line((poly_mouse.center), (vector[0] + poly_mouse.center[0], vector[1] + poly_mouse.center[1]), RED)
					# dist.append(d)
					collide = True
		
		if collide:
			for r in result:
				display.log(*r)
				# line((200,200), (dist[index][0] + 200, dist[index][1] + 200))
			# d_max = list(map(gjk_epa.dist, dist))
			# index = d_max.index(max(d_max))
			# # print(d_max[index], gjk_epa.angle(dist[index]))
			# printText(str(int(d_max[index])), (0,0))
			# printText(str(int(gjk_epa.angle(dist[index]))), (0,20))
			# line((200,200), (dist[index][0] + 200, dist[index][1] + 200))
			# poly_mouse.draw(GREEN)
		else:
			poly_mouse.draw(RED)
   
		pygame.display.flip()
		display.CLOCK.tick(frequency)
  
  
if __name__ == '__main__':
    run()