import pygame, math, sys, time, end, main
from pygame.locals import *
import os
game_folder = os.path.dirname(__file__)
img_folder= os.path.join(game_folder, "images")
#snd_folder= os.path.join(game_folder, "snd")
pygame.init()
screen = pygame.display.set_mode((1024, 768))
while 1:
    screen.fill((0,0,0))
    for event in pygame.event.get():
                if not hasattr(event, 'key'): continue
                if event.key == K_SPACE:
                    main.level1()
                elif event.key == K_ESCAPE: sys.exit(0)
    img = pygame.image.load(os.path.join(img_folder,"main_menu_image.png")).convert()
    screen.blit(img,(0,0))
    pygame.display.flip()
