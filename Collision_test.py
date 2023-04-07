frequency = 10
norm_noise = 20
time_predict = 2
dist_pred = 100
alg = 3

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
	way = [(90, 78), (90, 78), (90, 78), (90, 78), (90, 78),(90, 78), (90, 78), (90, 78), (90, 78), (90, 78), (90, 78), (90, 78),(90, 78), (90, 78), (88, 76), (80, 70), (79, 68), (79, 68), (79, 68), (79, 68), (79, 68), (83, 66), (95, 63), (112, 63), (136, 63), (156, 63), (176, 62), (199, 62), (218, 62), (236, 62), (252, 62), (273, 62), (297, 62), (322, 62), (351, 62), (378, 62), (405, 61), (429, 61), (455, 61), (486, 61), (515, 61), (541, 61), (564, 64), (590, 69), (603, 70), (641, 82), (661, 95), (682, 116), (696, 144), (698, 166), (698, 175), (691, 182), (677, 193), (648, 205), (622, 210), (607, 210), (575, 212), (545, 214), (516, 216), (483, 217), (462, 217), (439, 218), (419, 218), (394, 218), (356, 218), (316, 218), (281, 218), (256, 218), (234, 217), (209, 216), (182, 216), (160, 214), (141, 215), (130, 218), (123, 220), (112, 229), (106, 234), (102, 240), (102, 241), (99, 244), (92, 251), (88, 257), (84, 264), (80, 270), (78, 277), (77, 286), (75, 291), (74, 299), (74, 305), (74, 312), (74, 320), (76, 325), (78, 328), (81, 330), (86, 333), (109, 333), (116, 333), (121, 333), (128, 333), (137, 333), (150, 333), (161, 333), (170, 335), (176, 337), (187, 340), (197, 342), (216, 347), (238, 349), (248, 349), (257, 349), (266, 348), (276, 347), (284, 347), (291, 347), (302, 347), (315, 347), (330, 347), (354, 347), (377, 347), (399, 347), (420, 347), (442, 347), (470, 347), (505, 348), (533, 348), (553, 348), (574, 348), (598, 351), (623, 355), (650, 363), (674, 376), (681, 389), (687, 397), (692, 402), (697, 409), (700, 411), (702, 412), (704, 416), (705, 421), (708, 436), (706, 444), (696, 460), (683, 472), (675, 478), (653, 485), (621, 490), (596, 494), (574, 496), (544, 496), (523, 496), (506, 496), (482, 494), (459, 488), (433, 485), (410, 484), (402, 484), (388, 484), (368, 483), (348, 483), (323, 485), (295, 488), (271, 488), (251, 488), (232, 488), (221, 488), (208, 488), (194, 488), (181, 488), (174, 488), (165, 488), (150, 488), (137, 488), (134, 488), (128, 490), (115, 494), (106, 494), (98, 494), (90, 496), (81, 501), (78, 509), (79, 534), (82, 539), (82, 542), (86, 547), (97, 559), (118, 568), (147, 573), (155, 574), (166, 574), (176, 574), (196, 574), (217, 574), (241, 574), (257, 574), (275, 574), (289, 574), (303, 574), (314, 574), (328, 574), (341, 574), (352, 576), (365, 579), (379, 579), (395, 581), (410, 584), (425, 587), (436, 588), (460, 590), (477, 590), (493, 590), (512, 590), (529, 591), (545, 594), (562, 598), (573, 602), (583, 607), (618, 623), (646, 631), (655, 636), (665, 647), (670, 660), (672, 674), (672, 681), (670, 691), (668, 698), (652, 704), (629, 705), (613, 705), (576, 703), (542, 703), (534, 703), (531, 703), (524, 704), (511, 708), (492, 714), (473, 719), (457, 719), (441, 719), (425, 719), (407, 719), (389, 719), (371, 719), (352, 717), (329, 713), (322, 712), (317, 710), (303, 708), (281, 706), (266, 705), (257, 705), (243, 705), (224, 703), (209, 700), (200, 700), (190, 700), (178, 700), (167, 700), (153, 700), (141, 700), (137, 699), (132, 697), (128, 697), (122, 697), (117, 697), (111, 697), (103, 697), (93, 697), (78, 698), (73, 698), (71, 698), (66, 699)]
 
	display = Display()
	result = list()
	collision_list = set()
	tree = AABBTree()
	for i in range(len(allobj)):
		aabb = AABB(allobj[i].getMinMax())
		tree.add(aabb, i) 
	position = way[0]
	previousPosition = position
	position_list = queue.Queue(int(frequency/2))
	for _ in range(int(frequency/2)):
			position_list.put(position)
	
	for position in way:			
					
		display.SCREEN.fill(WHITE)
		# poly_mouse = Circle.makeFromMouse(20)
		# position = poly_mouse.center
		poly_mouse = Circle(position, 20)
		display.SCREEN.fill(WHITE)
		# Отрисовка 
		for i in range(len(allobj)):
			allobj[i].draw(BLACK)
		poly_mouse.draw(BLUE)
		collision = set()
		tmp_result = dict()
	
		match alg:
			case 1:		
				for obj in range(len(allobj)):
					dis, vector = allobj[obj].dictance_to_point(position)
					if dis < norm_noise + dist_pred:
						tmp_result[obj] = (dis, angle(vector, position))
						collision.add(obj)
						display.line(position, vector, RED)
					else:
						display.line(position, vector, GREEN)

			case 2:
				aabb = AABB(Circle(position, norm_noise + dist_pred).getMinMax())
				found_points = tree.overlap_values(aabb)
				for obj in found_points:						
					dis, vector = allobj[obj].dictance_to_point(position)
					if dis < norm_noise + dist_pred:
						# result.append((obj, distance(vector), angle(vector)))
						tmp_result[obj] = (dis, angle(vector, position))
						collision.add(obj)
						display.line(position, vector, RED)
					else:
						display.line(position, vector, GREEN)
					# result.append((i, distance(vector), angle(vector)))
		
			case 3:
				tmp_position = position_list.get()
				position_list.put(position)
				move = ((position[0] - tmp_position[0]), (position[1] - tmp_position[1])) 
				# move = ((position[0] - previousPosition[0]) / (1/frequency), (position[1] - previousPosition[1]) / (1/frequency)) 
				for i in range(1,time_predict  * frequency, 2):
					circle_result = dict()
					tmp_position = (position[0] + (move[0] / frequency) * i, position[1] + (move[1] / frequency)*i)
					tmp_circle = Circle(tmp_position,norm_noise)
					found_points = tree.overlap_values(AABB(tmp_circle.getMinMax()))
					# collide = False	
					for f in found_points:
						col = allobj[f].collide(tmp_circle)
						if col:
							_, project = allobj[f].dictance_to_point(tmp_circle.center)
							# collide = True
							dist = distance_point_point(position, project)
							ang = angle(position, project)
							if  f not in circle_result.keys() or (f in circle_result.keys() and circle_result[f][0] > dist):
								circle_result[f] = (dist, ang, project)
							collision.add(f)
					tmp_circle.draw(BLACK)
					tmp_result = tmp_result | circle_result
				for point in circle_result.values():
					display.line(position, point[2])
				
			case 4:
				tmp_position = position_list.get()
				position_list.put(position)
				move = ((position[0] - tmp_position[0]), (position[1] - tmp_position[1]))
				# move = ((position[0] - previousPosition[0]) / (1/frequency), (position[1] - previousPosition[1]) / (1/frequency)) 
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
							min_dist = float('inf')
							for p in points:
								dist = distance_point_point(p, position)
								if dist < min_dist:
									min_dist = dist 
									point = p
							if points :
								# point = (np.mean([p[0] for p in points]), np.mean([p[1] for p in points]))
								display.line(position, point, BLACK) 
								# result.append((f, min_dist, angle([position, point])))
								# tmp_result.append((obj, distance(vector), angle(vector)))
								tmp_result[f] = (min_dist, angle(point, position)) 
								collision.add(f)
								# for point in points:
								# 	display.line(poly_mouse.center, point, BLACK) 			
			case 'test':
				poly_mouse = Circle(position, norm_noise)
				for obj in range(len(allobj)):
					col = allobj[obj].collide(poly_mouse)
					if col:	
						collision.add(obj)
				result.append(list(collision - collision_list ))

		new_collision = collision - collision_list 
		if new_collision:
			print(*new_collision)
			collision_list = collision
		# dict_result = {r[0] : (r[1], r[2]) for r in tmp_result}
		dict_result = list()
		for c in new_collision:
			dict_result.append((c, tmp_result[c][0], tmp_result[c][1]))
		print(dict_result)
		result.append(dict_result)
		previousPosition = position
		pygame.display.flip()
		display.CLOCK.tick(10) 
	return result
		
if __name__ == '__main__':
	result = run(100)
	with open("result.txt", "w") as file:
		print(result, file=file)