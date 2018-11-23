#initialize the screen
import pygame, math, sys, level2, time
from pygame.locals import *
import os

game_folder = os.path.dirname(__file__)
img_folder= os.path.join(game_folder, "images")
WHITE= (255, 255, 255)
BLACK= (0, 0, 0)
RED= (255, 0, 0)
BLUE= (0, 0, 255)
GREEN= (0, 255, 0)
YELLOW= (255, 255, 0)

def level1(mpos=0):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1100, 750))
    #GAME CLOCK
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 75)
    win_font = pygame.font.Font(None, 50)
    win_condition = None
    win_text = font.render('', True, GREEN)
    loss_text = font.render('', True, RED)
    pygame.mixer.music.load('My_Life_Be_Like.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_pos(mpos)
    t0 = time.time()





    class CarSprite(pygame.sprite.Sprite):
        MAX_FORWARD_SPEED = 7.5
        MAX_REVERSE_SPEED = 7.5
        ACCELERATION = 2
        TURN_SPEED = 10

        def __init__(self, image, position):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = pygame.image.load(image).convert()
            self.mask= pygame.mask.from_surface(self.src_image)
            self.src_image.set_colorkey(WHITE)
            self.position = position
            self.speed = self.direction = 0
            self.k_left = self.k_right = self.k_down = self.k_up = 0

        def update(self, deltat):
            #SIMULATION
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_FORWARD_SPEED:
                self.speed = self.MAX_FORWARD_SPEED
            elif self.speed < -self.MAX_REVERSE_SPEED:
                self.speed = -self.MAX_REVERSE_SPEED
            elif self.k_up == 0 and self.k_down == 0 and self.speed != 0:
                if self.speed > 0:
                    self.speed -= 0.15
                    if abs(self.speed - 0.15) <= 0.15:
                        self.speed = 0
                elif self.speed < 0:
                    self.speed += 0.15
                    if abs(self.speed - 0.15) <= 0.15:
                        self.speed = 0

            self.direction += (self.k_right + self.k_left)
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            x += -self.speed*math.sin(rad)
            y += -self.speed*math.cos(rad)
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.mask= pygame.mask.from_surface(self.image)
            self.rect.center = self.position

    class PadSprite(pygame.sprite.Sprite):
        normal = pygame.image.load(os.path.join(img_folder,'barrier_new.png')).convert_alpha()
        #hit = pygame.image.load(os.path.join(img_folder,'collision.png')).convert_alpha()
        def __init__(self, position):
            super(PadSprite, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image=self.normal
            self.mask= pygame.mask.from_surface(self.image)
            '''
        def update(self, hit_list):
            if self in hit_list:
                self.image = self.hit
                self.mask= pygame.mask.from_surface(self.image)
            else:
                self.image = self.normal
                self.mask= pygame.mask.from_surface(self.image)
            '''

    class VerticalPad(pygame.sprite.Sprite):
        normal = pygame.image.load(os.path.join(img_folder,'barrier_v.png')).convert_alpha()
        def __init__(self, position):
            super(VerticalPad, self).__init__()
            self.rect = pygame.Rect(self.normal.get_rect())
            self.rect.center = position
            self.image = self.normal
            self.mask= pygame.mask.from_surface(self.image)
    pads = [
        PadSprite((125, 12.5)),
        PadSprite((475, 12.5)),
        PadSprite((725, 12.5)),
        PadSprite((975, 12.5)),
        PadSprite((125, 150)),
        PadSprite((375, 150)),
        PadSprite((625, 150)),
        PadSprite((725, 150)),
        VerticalPad((10, 125)),
        VerticalPad((1090, 125)),
        PadSprite((125, 300)),
        PadSprite((225, 300)),
        PadSprite((750, 300)),
        PadSprite((975, 300)),
        PadSprite((275, 450)),
        PadSprite((525, 450)),
        PadSprite((775, 450)),
        VerticalPad((10, 375)),
        VerticalPad((1090, 375)),
        PadSprite((125, 600)),
        PadSprite((325, 600)),
        PadSprite((775, 600)),
        PadSprite((900, 600)),
        PadSprite((975, 600)),
        VerticalPad((10, 625)),
        VerticalPad((1090, 625)),
        PadSprite((275, 737.5)),
        PadSprite((525, 737.5)),
        PadSprite((775, 737.5)),
        PadSprite((975, 737.5)),
    ]
    pad_group = pygame.sprite.RenderPlain(*pads)

    class Trophy(pygame.sprite.Sprite):
        def __init__(self, position):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(os.path.join(img_folder,'trophy.png')).convert_alpha()
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = position
        def draw(self, screen):
            screen.blit(self.image, self.rect)

    trophies = [Trophy((285,0))]
    trophy_group = pygame.sprite.RenderPlain(*trophies)

    #BACKGROUND
    background= pygame.image.load(os.path.join(img_folder, "bgpic2.png")).convert()
    background_rect=background.get_rect()

    # CREATE A CAR AND RUN
    rect = screen.get_rect()
    car = CarSprite(os.path.join(img_folder,'red_car_3.png'), (50, 730))
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
            #print(down)
            #print(event.key)
            if win_condition == None:
                if event.key == K_RIGHT: car.k_right = down * -5
                elif event.key == K_LEFT: car.k_left = down * 5
                elif event.key == K_UP: car.k_up = down * 1
                elif event.key == K_DOWN: car.k_down = down * -1
                elif event.key == K_ESCAPE: sys.exit(0) # quit the game
            elif win_condition == True and event.key == K_SPACE: level2.level2(mpos+round(pygame.mixer.music.get_pos()/1000))
            elif win_condition == False and event.key == K_SPACE:
                level1(mpos+round(pygame.mixer.music.get_pos()/1000))
                t0 = t1
            elif event.key == K_ESCAPE: sys.exit(0)


        #COUNTDOWN TIMER
        seconds = round((20 - dt),2)
        if win_condition == None:
            timer_text = font.render(str(seconds), True, YELLOW)
            if seconds <= 0:
                win_condition = False
                timer_text = font.render("Time!", True, RED)
                loss_text = win_font.render('Press Space to Retry', True, RED)


        #RENDERING
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        car_group.update(deltat)
        collisions = pygame.sprite.groupcollide(car_group, pad_group, False, False, pygame.sprite.collide_mask)
        if collisions != {} and win_condition != True:
            win_condition = False
            timer_text = font.render("Crash!", True, RED)
            car.image = pygame.image.load(os.path.join(img_folder,'collision.png')).convert_alpha()
            loss_text = win_font.render('Press Space to Retry', True, RED)
            seconds = 0
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            car.k_right = 0
            car.k_left = 0

        trophy_collision = pygame.sprite.groupcollide(car_group, trophy_group, False, True)
        if trophy_collision != {}:
            seconds = seconds
            timer_text = font.render("Finished!", True, GREEN)
            win_condition = True
            car.MAX_FORWARD_SPEED = 0
            car.MAX_REVERSE_SPEED = 0
            win_text = win_font.render('Press Space to Advance', True, GREEN)
            if win_condition == True:
                car.k_right = -5


        #pad_group.update(collisions)
        pad_group.draw(screen)
        car_group.draw(screen)
        trophy_group.draw(screen)
        #Counter Render
        screen.blit(timer_text, (20,60))
        screen.blit(win_text, (330, 660))
        screen.blit(loss_text, (330, 660))
        pygame.display.flip()
