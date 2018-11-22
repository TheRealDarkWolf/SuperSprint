import pygame, math, sys, time, end, main
from pygame.locals import *
from hangman.hangman import main as mainn
import os
game_folder = os.path.dirname(__file__)
img_folder= os.path.join(game_folder, "images")

BLACK= (0, 0, 0)
RED= (255, 0, 0)
BLUE= (0, 0, 255)
GREEN= (0, 255, 0)
YELLOW= (255, 255, 0)
#snd_folder= os.path.join(game_folder, "snd")
pygame.init()
screen = pygame.display.set_mode((1024, 768))
while 1:
    screen.fill(BLACK)
    for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit(0)
                if not hasattr(event, 'key'): continue
                if event.key == K_SPACE:
                    main.level1()
                elif event.key == K_ESCAPE: sys.exit(0)
                elif event.key == K_RETURN:
                    pygame.display.quit()
                    mainn()
                    break
    try:
        img = pygame.image.load(os.path.join(img_folder,"MainMenuFinal.png")).convert()
        screen.blit(img,(0,0))
        pygame.display.flip()
    except:
        print("Thanks for playing Hangman")
        break

