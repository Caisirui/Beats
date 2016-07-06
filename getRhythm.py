# -*- coding: utf-8 -*-
import pygame
import time
import sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480



pygame.init()
SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Tetromino for Idiots')
pygame.mixer.music.load('bgm.ogg')
pygame.mixer.music.play(-1, 0.0)
t0 = time.clock()
file = open('./beats/rhythm1.txt', 'w')


while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            file.write(str(time.clock() - t0) + '\n')
            print(time.clock() - t0)
        elif event.type == QUIT:
            file.close()
            pygame.quit()
            sys.exit()
    pygame.display.update()
