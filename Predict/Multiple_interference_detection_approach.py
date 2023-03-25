frequency = 1
norm_noise = 0

from math import sqrt
import sys
import random as rd

import numpy as np

import pygame
from pygame.locals import *


from Graphic import Display, Poly, Circle, BLACK, WHITE, BLUE, GREEN, RED



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
		# move = sqrt((position[0] - previousPosition[0])**2 + (position[1] - previousPosition[1])**2) / (1/frequency)
		move = ((position[0] - previousPosition[0]) / frequency, (position[1] - previousPosition[1]) / frequency) 
		for i in range(1,4):
			Circle((position[0] + move[0]*i, position[1] + move[1]*i),20).draw(GREEN)
		print(move)
  
		for i in range(len(allobj)):
			allobj[i].draw(BLACK)
		poly_mouse.draw(RED)
			
		previousPosition = position
		pygame.display.flip()
		display.CLOCK.tick(frequency)
  
  
if __name__ == '__main__':
    run()