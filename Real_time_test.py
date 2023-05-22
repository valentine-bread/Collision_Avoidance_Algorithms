frequency = 15
norm_noise = 20
time_predict = 3
alg = 4

from math import sqrt, radians, sin, cos
import sys
import random as rd
import queue
import numpy as np

import pygame
from pygame.locals import *

from aabbtree import AABB, AABBTree
# from GJK import gjk_epa

from distance_project import distance, angle, distance_point_point

# from Graphic.graphic_sat import Display
from Graphic.graphic_sat import Display, Poly, Circle, BLACK, WHITE, BLUE, GREEN, RED
rd.seed(456)

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

def run(quantity):	    
    
	allobj = list()
	for _ in range(quantity):
		h, w = rd.randint(1, 100), rd.randint(1, 100)
		x, y = rd.randint(0, 800), rd.randint(0, 800)
		polygon = [(x,y),(x+0,y+h),(x+w,y+h),(x+w,y+0)]
		angle_degrees = rd.randint(0, 360)
		if angle_degrees != 0:
			angle_radians = radians(angle_degrees)
			relative_points = [(0,0),(0,h),(w,h),(w,0)]
			rotated_points = [(
					relative_point[0] * cos(angle_radians) - relative_point[1] * sin(angle_radians),
					relative_point[0] * sin(angle_radians) + relative_point[1] * cos(angle_radians),)
                for relative_point in relative_points]
			polygon = [(point[0] + x, point[1] + y) for point in rotated_points]
		else:
			polygon = [(x,y),(x+0,y+h),(x+w,y+h),(x+w,y+0)]
		allobj.append(Poly(polygon))
	for _ in range(int(quantity/10)):
		x, y, r = rd.randint(0, 800), rd.randint(0, 800), rd.randint(1, 40)
		allobj.append(Circle((x,y),r))
		
	# way = [(i,i) for i in range(800)]		
 
	
	display = Display()
	result = list()
	tree = AABBTree()
	for i in range(len(allobj)):
		aabb = AABB(allobj[i].getMinMax())
		tree.add(aabb, i) 
	position = pygame.mouse.get_pos()
	position_log_list = list()
	position_list = queue.Queue(int(frequency/2))
	for _ in range(int(frequency/2)):
			position_list.put(position)
	
	while True:
		position_log_list.append(position)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					sys.exit()
				elif event.key == K_UP:
					print(position_log_list)
				elif event.key == K_DOWN:
					pass
				elif event.key == K_LEFT:
					pass
				elif event.key == K_RIGHT:
					pass
				
					
		display.SCREEN.fill(WHITE)
		poly_mouse = Circle.makeFromMouse(20)
		position = poly_mouse.center
		display.SCREEN.fill(WHITE)
		# Отрисовка 
		for i in range(len(allobj)):
			allobj[i].draw(BLACK)
		poly_mouse.draw(BLUE)
  
     
		match alg:
			case 1:			
				for obj in range(len(allobj)):
					dis, vector = allobj[obj].dictance_to_point(position)
					if dis < norm_noise + 100:
						result.append((obj, distance(vector), angle(vector)))
						display.line(position, vector, RED)
					else:
						display.line(position, vector, GREEN)

			case 2:
				aabb = AABB(Circle(position, norm_noise + 100).getMinMax())
				found_points = tree.overlap_values(aabb)
				for obj in found_points:						
					dis, vector = allobj[obj].dictance_to_point(position)
					if dis < norm_noise + 100:
						result.append((obj, distance(vector), angle(vector)))
						display.line(position, vector, RED)
					else:
						display.line(position, vector, GREEN)
					result.append((i, distance(vector), angle(vector)))
		
			case 3:
				tmp_position = position_list.get()
				position_list.put(position)
				move = ((position[0] - tmp_position[0]), (position[1] - tmp_position[1])) 
				for i in range(1,time_predict  * frequency, 2):
					tmp_position = (position[0] + (move[0] / frequency) * i, position[1] + (move[1] / frequency)*i)
					tmp_circle = Circle(tmp_position,norm_noise)
					found_points = tree.overlap_values(AABB(tmp_circle.getMinMax()))
					result = list()
					collide = False	
					for f in found_points:
						col = allobj[f].collide(tmp_circle)
						if col:
							dist, vector = allobj[f].dictance_to_point(tmp_circle.center)
							display.line(position, vector, GREEN)
							collide = True
							result.append((f, dist, angle([position, vector])))
							# print((f, dist, angle([position, vector])))
					tmp_circle.draw(BLACK)			

			case 4:
				tmp_position = position_list.get()
				position_list.put(position)
				move = ((position[0] - tmp_position[0]), (position[1] - tmp_position[1])) 
				if move != (0,0):
					tmp_position = (position[0] + (move[0] * time_predict* frequency  * (1/frequency)), position[1] + (move[1] * time_predict* frequency  * (1/frequency)))		
					tmp_vector = normalize(orthogonal(edge_direction(poly_mouse.center, tmp_position)))
					volume_rect = Poly([(position[0] + tmp_vector[0] * norm_noise, position[1] + tmp_vector[1] * norm_noise),
						(position[0] - tmp_vector[0] * norm_noise, position[1] - tmp_vector[1] * norm_noise),
						(tmp_position[0] - tmp_vector[0] * norm_noise, tmp_position[1] - tmp_vector[1] * norm_noise),
						(tmp_position[0] + tmp_vector[0] * norm_noise, tmp_position[1] + tmp_vector[1] * norm_noise)])
					volume_rect.draw(GREEN)
					projection_circle = Circle(tmp_position, 20)
					for obj in [volume_rect]:		
						col_result = tree.overlap_values(AABB(obj.getMinMax())) 
						obj.draw(GREEN if col_result else RED)
						for f in col_result:
							points = allobj[f].intersection(obj)		
							# min_dist = float('inf')							
							# for p in points:
							# 	dist = distance_point_point(p, position)
							# 	if dist < min_dist:
							# 		min_dist = dist 
							# 		point = p
							# point = (np.mean([p[0] for p in points]), np.mean([p[1] for p in points]))
							if points:
								point = sorted(points, key=lambda p: distance_point_point(p, position))[0]
								display.line(poly_mouse.center, point, BLACK) 
							# for point in points:
							# 	display.line(poly_mouse.center, point, BLACK) 			


		
		pygame.display.flip()
		display.CLOCK.tick(frequency) 
	return result
		
if __name__ == '__main__':
	run(100)