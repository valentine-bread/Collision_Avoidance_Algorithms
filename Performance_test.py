frequency = 2
norm_noise = 20
time_predict = 3

from math import sqrt, radians, sin, cos
import sys
import random as rd
import queue
import numpy as np
from aabbtree import AABB, AABBTree
from distance_project import distance, angle
from Graphic.no_graphic_sat import Poly, Circle, BLACK, WHITE, BLUE, GREEN, RED
rd.seed(11111)

def normalize(vector):
	if vector == (0,0): return vector
	norm = sqrt(vector[0] ** 2 + vector[1] ** 2)
	return vector[0] / norm, vector[1] / norm

def dot(vector1, vector2):
	return vector1[0] * vector2[0] + vector1[1] * vector2[1]

def edge_direction(point0, point1):
	return point1[0] - point0[0], point1[1] - point0[1]

def orthogonal(vector):
	return vector[1], -vector[0]

def run(alg, quantity):	    
    
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
		
	way = [(i,i) for i in range(800)]
	result = list()	
     
	match alg:
		case 1:		
			for position in way:
				for obj in range(len(allobj)):
					dis, vector = allobj[obj].dictance_to_point(position)
					if dis < norm_noise + 100:
						result.append((obj, distance(vector), angle(vector)))
		case 2:
			tree = AABBTree()
			for i in range(len(allobj)):
				aabb = AABB(allobj[i].getMinMax())
				tree.add(aabb, i) 
     
			for position in way:
				poly_mouse = Circle(position, 20)

				aabb = AABB(Circle(position, norm_noise + 100).getMinMax())
				found_points = tree.overlap_values(aabb)
				for obj in found_points:						
					dis, vector = allobj[obj].dictance_to_point(position)
					if dis < norm_noise + 100:
						result.append((obj, distance(vector), angle(vector)))
		case 3:
			tree = AABBTree()
			for i in range(len(allobj)):
				aabb = AABB(allobj[i].getMinMax())
				tree.add(aabb, i) 
			position_list = queue.Queue(int(frequency/2))
			for _ in range(int(frequency/2)):
				position_list.put(way[0])
     
			for position in way:
				poly_mouse = Circle(position, 1)
				# Алгоритм обнаружения множественных помех----
				tmp_position = position_list.get()
				position_list.put(position)
				move = ((position[0] - tmp_position[0]), (position[1] - tmp_position[1])) 
				for i in range(1,time_predict  * frequency, 2):
					tmp_position = (position[0] + (move[0] * 30 / frequency)*i, position[1] + (move[1] * 30 / frequency)*i)
					tmp_circle = Circle(tmp_position,norm_noise)
					found_points = tree.overlap_values(AABB(tmp_circle.getMinMax()))
					result = list()
					collide = False	
					for f in found_points:
						col = allobj[f].collide(tmp_circle)
						if col:
							dist, vector = allobj[f].dictance_to_point(tmp_circle.center)
							collide = True
							result.append((f, dist, angle([position, vector])))			
				# -----------------------------------------------
		case 4:
			tree = AABBTree()
			for i in range(len(allobj)):
				aabb = AABB(allobj[i].getMinMax())
				tree.add(aabb, i) 
			position_list = queue.Queue(int(frequency/2))
			for _ in range(int(frequency/2)):
				position_list.put(way[0])
     
			for position in way:
				poly_mouse = Circle(position, 1)
				# Алгоритм------------------------------------------------
				tmp_position = position_list.get()
				position_list.put(position)
				move = ((position[0] - tmp_position[0]), (position[1] - tmp_position[1])) 
				if move != (0,0):
					tmp_position = (position[0] + (move[0] * 30 * time_predict* frequency  * (1/frequency)), position[1] + (move[1] * 30 * time_predict* frequency  * (1/frequency)))		
					tmp_vector = normalize(orthogonal(edge_direction(poly_mouse.center, tmp_position)))
					volume_rect = Poly([(position[0] + tmp_vector[0] * norm_noise, position[1] + tmp_vector[1] * norm_noise),
						(position[0] - tmp_vector[0] * norm_noise, position[1] - tmp_vector[1] * norm_noise),
						(tmp_position[0] - tmp_vector[0] * norm_noise, tmp_position[1] - tmp_vector[1] * norm_noise),
						(tmp_position[0] + tmp_vector[0] * norm_noise, tmp_position[1] + tmp_vector[1] * norm_noise)])
					projection_circle = Circle(tmp_position, 20)
					# result = list()
					# for obj in [projection_circle, volume_rect, poly_mouse]:		
					for obj in [volume_rect]:		
						col_result = tree.overlap_values(AABB(obj.getMinMax())) 
						# result += col_result
						# obj.draw(GREEN if col_result else RED)
						if col_result:
							# print(result)
							for f in col_result:
								points = allobj[f].intersection(obj) 			
				# -----------------------------------------------
	return result
		

from time import process_time
import matplotlib.pyplot as plt

if __name__ == '__main__':
	result_test = list()
	for a in range(1, 5):
		tmp_result = list()
		x = range(10, 501, 10)
		for q in x:
			t1_start = process_time() 
			run(alg = a, quantity = q)
			t1_stop = process_time()
			# print("Elapsed time:", t1_stop, t1_start)
			print("Test:",q, "\nTime:", t1_stop - t1_start) 
			tmp_result.append(t1_stop - t1_start)
		result_test.append(tmp_result)
	print(result_test)
	for y,i in zip(result_test, ['1','2','3','4']):
		plt.plot(x,y, label = 'Algoritm' + i) 
	plt.xlabel('Количество объектов')
	plt.ylabel('Время (сек.)')
	plt.legend()
	plt.show()
