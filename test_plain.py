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
		Poly([(0, 0), (0, 150), (10, 150), (10, 0)])
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
				col, (pol, vector) = allobj[i].collide(poly_mouse)
				if col:
					result.append((i, gjk_epa.dist(vector), gjk_epa.angle(vector)))
					display.line(((400,400)), (vector[0] + 400, vector[1] + 400), RED)
					# dist.append(d)
					pol = Poly(pol)
					pol.add(400,400)
					pol.draw(BLACK)
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