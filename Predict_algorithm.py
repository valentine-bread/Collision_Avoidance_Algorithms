frequency = 10
norm_noise = 0
time_predict = 4

from math import sqrt
import sys
import random as rd

import numpy as np

import pygame
from pygame.locals import *

from aabbtree import AABB, AABBTree
from GJK import gjk_epa

#sys.path.append(r"C:/Study/Мага ВКР/НИР весна 23/Test_alg/Graphic")

from Graphic.graphic import Display, Poly, Circle, BLACK, WHITE, BLUE, GREEN, RED

def normalize(vector):
    # if vector == (0,0): return vector
    # norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
    # return vector[0] / norm, vector[1] / norm
    return vector / np.linalg.norm(vector)

def dot(vector1, vector2):
    """
    Точка (или скалярное) произведение двух векторов
    """
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]


def edge_direction(point0, point1):
    """
    Вектор, идущий из point0 в point1
    """
    return point1[0] - point0[0], point1[1] - point0[1]


def orthogonal(vector):
    """
    Новый вектор, ортогональный данному вектору
    """
    return vector[1], -vector[0]

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
	  	
	previousPosition = pygame.mouse.get_pos()
	
	allobj = list(wall)
	allobj += furniture
	
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

		position = poly_mouse.center	
		move = ((position[0] - previousPosition[0]) / frequency, (position[1] - previousPosition[1]) / frequency) 
		# move = (move[0] if move[0] != 0 else 0.00001, move[1] if move[1] != 0 else 0.00001)
  
		# Алгоритм обнаружения множественных помех----
		# for i in range(1,time_predict  * frequency):
		# 	tmp_position = (position[0] + move[0]*i, position[1] + move[1]*i)
		# 	tmp_circle = Circle(tmp_position,20)
		# 	found_points = tree.overlap_values(AABB(tmp_circle.getMinMax()))
		# 	result = list()
		# 	collide = False	
		# 	for f in found_points:
		# 		col, vector = allobj[f].collide(tmp_circle)
		# 		if col:
		# 			result.append((f, gjk_epa.dist(vector), gjk_epa.angle(vector)))
		# 			collide = True
		# 	tmp_circle.draw(GREEN if collide else RED)			
		#-----------------------------------------------
		
		# Алгоритм помехи с качающимся объемом
		# if move != (0,0):
		# 	tmp_position = (position[0] + (move[0] * time_predict  * frequency), position[1] + (move[1] * time_predict  * frequency))		
		# 	tmp_vector = normalize(orthogonal(edge_direction(poly_mouse.center, tmp_position)))
		# 	volume_rect = Poly([(poly_mouse.center[0] + tmp_vector[0] * 20, poly_mouse.center[1] + tmp_vector[1] * 20),
		# 		(poly_mouse.center[0] - tmp_vector[0] * 20, poly_mouse.center[1] - tmp_vector[1] * 20),
		# 		(tmp_position[0] - tmp_vector[0] * 20, tmp_position[1] - tmp_vector[1] * 20),
		# 		(tmp_position[0] + tmp_vector[0] * 20, tmp_position[1] + tmp_vector[1] * 20)])

		# 	volume_rect.draw(GREEN)
		# 	projection_circle = Circle(tmp_position, 20)
		# 	# projection_circle.draw(GREEN)
		# 	result = list()
		# 	for obj in [projection_circle, volume_rect]:			
		# 		found_points = tree.overlap_values(AABB(obj.getMinMax()))
		# 		collide = False
		# 		for f in found_points:
		# 			col, vector = allobj[f].collide(obj)
		# 			if col:
		# 				result.append((f, gjk_epa.dist(vector), gjk_epa.angle(vector)))
		# 				collide = True
		# 		obj.draw(GREEN if collide else RED)
		# 	print(result)
		#----------------------------------------------
		
  
		# Алгоритм 
  

		#
  
  
		
		previousPosition = position
  		# Отрисовка 
		for i in range(len(allobj)):
			allobj[i].draw(BLACK)
		poly_mouse.draw(BLUE)
		
		pygame.display.flip()
		display.CLOCK.tick(frequency)
  
  
if __name__ == '__main__':
    run()