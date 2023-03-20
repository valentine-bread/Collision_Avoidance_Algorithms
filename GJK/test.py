"""
Pygame script to test that the algorithm works.
"""
from math import sqrt
import sys

import pygame
from pygame.locals import *

import gjk_epa



pygame.init()
SCREEN = pygame.display.set_mode((800, 600))
CLOCK = pygame.time.Clock()

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)

def run():
    poly_list = [(
        ( 00 + 400,  50 + 300),
        (-50 + 400,  50 + 300),
        (-50 + 400,   0 + 300)
    )]
    circle_list = [#((400, 300), 100),
                   ((600, 100), 100)
                       ]

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
     
        for p in poly_list:
            col, d = gjk_epa.collidePolyCircle(p, poly_mouse)
            dist.append(d)
            collide.append(col)
            polygon(p)
            
        for c in circle_list:
            col, d = gjk_epa.collideCircleCircle(poly_mouse, c)
            dist.append(d)
            collide.append(col)
            circle(c)

        if any(collide):
            d_max = list(map(lambda x: sqrt(x[0] ** 2 + x[1] ** 2), dist))
            index = d_max.index(max(d_max))
            print(d_max[index])
            line((200,200), (dist[index][0] + 200, dist[index][1] + 200))
            circle(poly_mouse, GREEN)
        else:
            circle(poly_mouse, RED)
        

        
        pygame.display.flip()
        CLOCK.tick(60)

def makeCircleFromMouse():
    pos = pygame.mouse.get_pos()

    return (
        ((0 + pos[0], 0 + pos[1]), 20)
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