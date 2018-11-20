#initialize the screen
import pygame, math, sys, time, end
from pygame.locals import *
import os
from PIL import Image


game_folder = os.path.dirname(__file__)
img_folder= os.path.join(game_folder, "images")
def level1():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1585, 900))
    #GAME CLOCK
    bg = pygame.image.load(os.path.join(img_folder,'bg.png')).convert()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 75)
    win_font = pygame.font.Font(None, 50)
    win_condition = None
    win_text = font.render('', True, (0, 255, 0))
    loss_text = font.render('', True, (255, 0, 0))
    #pygame.mixer.music.load('My_Life_Be_Like.mp3')
    #pygame.mixer.music.play(-1)
    t0 = time.time()
    bgimgpix = Image.open(os.path.join(img_folder,'bg.png'))

    pixels = bgimgpix.load() # this is not a list, nor is it list()'able
    width, height = bgimgpix.size
    
    



    class CarSprite(pygame.sprite.Sprite):
        MAX_FORWARD_SPEED = 7.5
        MAX_REVERSE_SPEED = 7.5
        ACCELERATION = 2
        TURN_SPEED = 10

        def __init__(self, image, position):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = pygame.image.load(image).convert_alpha()
            self.position = position
            self.speed = 0
            self.direction = -90
            self.k_left = self.k_right = self.k_down = self.k_up = 0

        def update(self, deltat):
            #SIMULATION
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_FORWARD_SPEED:
                self.speed = self.MAX_FORWARD_SPEED
            elif self.speed < -self.MAX_REVERSE_SPEED:
                self.speed = -self.MAX_REVERSE_SPEED
            elif self.k_up == 0 and self.k_down == 0:
                if self.speed > 0:
                    self.speed -= 0.15
                elif self.speed < 0:
                    self.speed += 0.15
            self.direction += (self.k_right + self.k_left)
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            x += -self.speed*math.sin(rad)
            y += -self.speed*math.cos(rad)
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position

    # CREATE A CAR AND RUN
    rect = screen.get_rect()
    car = CarSprite(os.path.join(img_folder,'car.png'), (500, 740))
    car_group = pygame.sprite.RenderPlain(car)

    #THE GAME LOOP
    while 1:
        #USER INPUT
        t1 = time.time()
        dt = t1-t0

        deltat = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit(0)
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN
            if win_condition == None:
                if event.key == K_RIGHT: car.k_right = down * -5
                elif event.key == K_LEFT: car.k_left = down * 5
                elif event.key == K_UP: car.k_up = down * 0.75
                elif event.key == K_DOWN: car.k_down = down * -0.75
                elif event.key == K_ESCAPE: sys.exit(0) # quit the game
            elif win_condition == True and event.key == K_SPACE: end.end_game()
            elif win_condition == False and event.key == K_SPACE:
                level1()
                t0 = t1
            elif event.key == K_ESCAPE: sys.exit(0)
            

        #COUNTDOWN TIMER
        seconds = round(dt,2)
        timer_text = font.render(str(seconds), True, (255,255,0))
        
        x, y = (car.position)
        pixx = pixels[x,y]
        if pixx != (0,0,0):
            win_condition = False
            timer_text = font.render("Crash!", True, (255,0,0))
            car.src_image = pygame.image.load(os.path.join(img_folder,'collision.png')).convert_alpha()
            loss_text = win_font.render('Press Space to Retry', True, (255,0,0))
            seconds = 0
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            car.k_right = 0
            car.k_left = 0

        #print(pixx)
        #print(car_group)
        #RENDERING
        screen.blit(bg, [0, 0])
        car_group.update(deltat)
        


       
        car_group.draw(screen)
        #Counter Render
        screen.blit(timer_text, (20,60))
        screen.blit(win_text, (250, 700))
        screen.blit(loss_text, (250, 700))
        pygame.display.flip()

