frequency = 2
norm_noise = 20
time_predict = 3


from math import sqrt
import sys
import random as rd
import queue
import numpy as np

import pygame
from pygame.locals import *

from aabbtree import AABB, AABBTree
from GJK import gjk_epa

#sys.path.append(r"C:/Study/Мага ВКР/НИР весна 23/Test_alg/Graphic")

from Graphic.graphic_gik_epa import Display, Poly, Circle, BLACK, WHITE, BLUE, GREEN, RED

def normalize(vector):
    if vector == (0,0): return vector
    norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector[0] / norm, vector[1] / norm
    # return vector / np.linalg.norm(vector)

def dot(vector1, vector2):
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]


def edge_direction(point0, point1):
    return point1[0] - point0[0], point1[1] - point0[1]


def orthogonal(vector):
    return vector[1], -vector[0]

def collide_test(tree, allobj, obj):
	result = list()
	found_points = tree.overlap_values(AABB(obj.getMinMax()))
	collide = False
	for f in found_points:
		col, vector = allobj[f].collide(obj)
		if col:
			# result.append((f, gjk_epa.dist(vector), gjk_epa.angle(vector)))
			result.append((f, vector))
			collide = True
	return result

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
	  	
	previousPosition = (0,0)
	
	allobj = list(wall)
	allobj += furniture
	
	tree = AABBTree()
	for i in range(len(allobj)):
		aabb = AABB(allobj[i].getMinMax())
		tree.add(aabb, i)   


	display = Display()
	position_list = queue.Queue(int(frequency/2))
	for _ in range(int(frequency/2)):
			position_list.put(pygame.mouse.get_pos())
	

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
		tmp_position = position_list.get()
		position_list.put(position)

		# move = ((position[0] - previousPosition[0]) / (1/frequency), (position[1] - previousPosition[1]) / (1/frequency)) 
		# move = (move[0] if move[0] != 0 else 0.00001, move[1] if move[1] != 0 else 0.00001)
		move = ((position[0] - tmp_position[0]), (position[1] - tmp_position[1])) 
  
		# Алгоритм обнаружения множественных помех----
		# for i in range(1,time_predict  * frequency, 2):
		# 	tmp_position = (position[0] + (move[0] / frequency)*i, position[1] + (move[1] / frequency)*i)
		# 	tmp_circle = Circle(tmp_position,norm_noise)
		# 	found_points = tree.overlap_values(AABB(tmp_circle.getMinMax()))
		# 	result = list()
		# 	collide = False	
		# 	for f in found_points:
		# 		col, vector = allobj[f].collide(tmp_circle)
		# 		if col:
		# 			result.append((f, gjk_epa.dist(vector), gjk_epa.angle(vector)))
		# 			norm_vector = normalize(tuple(vector))
		# 			dist = gjk_epa.dist(vector)
		# 			display.line(poly_mouse.center,  (((tmp_circle.radius - dist) * norm_vector[1]) + tmp_circle.center[0], 
        #                                				((tmp_circle.radius - dist) * norm_vector[0]) + tmp_circle.center[1]), BLACK)
		# 			collide = True
		# 	tmp_circle.draw(GREEN if collide else RED)			
		# -----------------------------------------------
		
		# Алгоритм помехи с качающимся объемом
		if move != (0,0):
			tmp_position = (position[0] + (move[0] * time_predict* frequency  * (1/frequency)), position[1] + (move[1] * time_predict* frequency  * (1/frequency)))		
			tmp_vector = normalize(orthogonal(edge_direction(poly_mouse.center, tmp_position)))
			volume_rect = Poly([(position[0] + tmp_vector[0] * norm_noise, position[1] + tmp_vector[1] * norm_noise),
				(position[0] - tmp_vector[0] * norm_noise, position[1] - tmp_vector[1] * norm_noise),
				(tmp_position[0] - tmp_vector[0] * norm_noise, tmp_position[1] - tmp_vector[1] * norm_noise),
				(tmp_position[0] + tmp_vector[0] * norm_noise, tmp_position[1] + tmp_vector[1] * norm_noise)])
			volume_rect.draw(GREEN)
			projection_circle = Circle(tmp_position, 20)
			result = list()
			for obj in [projection_circle, volume_rect, poly_mouse]:			
				col_result = collide_test(tree, allobj, obj)
				# col_result = 
				result += col_result
				obj.draw(GREEN if col_result else RED)
				print(result)
				# for r in result:
				# 	display.line((200 + r[1][0],150 + r[1][1]),(200,200), BLACK)
		# ----------------------------------------------
  
		# Алгоритм аналитический
		# poly_mouse = Circle.makeFromMouse(1)
		# tmp_position = (position[0] + (move[0] * time_predict  * frequency), position[1] + (move[1] * time_predict  * frequency))		
		# tmp_vector = normalize(orthogonal(edge_direction(poly_mouse.center, tmp_position)))	
		# move = (1,1) if move == (0,0) else move
		# radius_projection = norm_noise / (sqrt(move[0] ** 2 + move[1] ** 2)) if (sqrt(move[0] ** 2 + move[1] ** 2)) > 1 else 1
		# # print(radius_projection)
		# volume_rect = Poly([(position[0] + tmp_vector[0] * 1, position[1] + tmp_vector[1] * 1),
		# 	(position[0] - tmp_vector[0] * 1, position[1] - tmp_vector[1] * 1),
		# 	(tmp_position[0] - tmp_vector[0] * radius_projection, tmp_position[1] - tmp_vector[1] * radius_projection),
		# 	(tmp_position[0] + tmp_vector[0] * radius_projection, tmp_position[1] + tmp_vector[1] * radius_projection)])
		# volume_rect.draw(GREEN)
		# projection_circle = Circle(tmp_position, radius_projection)
		# result = list()
		# for obj in [projection_circle, volume_rect, poly_mouse]:			
		# 	col_result = collide_test(tree, allobj, obj)
		# 	result += col_result
		# 	obj.draw(GREEN if col_result else RED)
		# 	# print(result)
		#----------------------------------------------
		
  

		previousPosition = position
  		# Отрисовка 
		for i in range(len(allobj)):
			allobj[i].draw(BLACK)
		poly_mouse.draw(BLUE)
		
		pygame.display.flip()
		display.CLOCK.tick(frequency)
  
  
if __name__ == '__main__':
    run()