# -*- coding: utf-8 -*-
import pygame
import time
import os
import sys
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 721
WINDOWHEIGHT = 700

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

COLORS = (WHITE, RED, GREEN, BLUE)
OFFSET = (0, 3)
fps_clock = pygame.time.Clock()

pygame.init()
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
JUDGE_LINE = pygame.image.load('judge_line.png')
judge_line_rect = JUDGE_LINE.get_rect()
judge_line_rect.bottom = 700
UP_ARROW = pygame.image.load('up_arrow.png')
rect = UP_ARROW.get_rect()
rect.left = 10

block = pygame.Rect(0, 0, 100, 5)
time_0 = time.clock()
print(os.listdir('./.idea'))
print('abc.txt'[0:-4] + '.mp3')
while True:

    SCREEN.fill(BLACK)
    SCREEN.blit(UP_ARROW, rect)
    rect = rect.move(OFFSET)
    if rect.bottom >= 675:
        print(time.clock() - time_0)
        break
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            print(event.key)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    SCREEN.blit(JUDGE_LINE, judge_line_rect)
    pygame.display.update()
    fps_clock.tick(FPS)