# || IMPORT STATEMENTS ||

import pygame, sys
from pygame.locals import *
from random import randint

# || CONSTANTS ||

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1850
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)

# || PYGAME SETUP ||

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# || CLASSES ||

#functionality:
#mathematics determine position of paper airplane after thrown

def v_y(t, vy_o):
    '''projectile motion vertical velocity function for the plane'''
    return ((vy_o*t+0.2*t**2)/100)

def v_x(t, vx_o, touching_ground=False):
    '''projectile motion horizontal velocity function for the plane'''
    final = vx_o
    # if touching_ground:
    #     if final != 0:
    #         return(final-final*0.5, 1)
    #     elif final == 0:
    #         return tuple(0, 0)
    return (final)

class Plane(pygame.sprite.Sprite):
    def __init__ (self, velocity_x=randint(6,9), velocity_y=randint(1,4)):
        pygame.sprite.Sprite.__init__(self)
        #SPEEDS
        self.horizontal_speed = velocity_x
        self.vertical_speed = velocity_y

        #self.image = pygame.image.load("plane.png").convert()
        self.image = pygame.Surface((25,25)) #to be replaced
        self.image.fill(WHITE) #to be replaced
        
        #self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 2)

        self.keep_moving = True

    def update(self, time):
        velocity_x = v_x(time, self.horizontal_speed)
        if self.keep_moving:
            self.rect.x += velocity_x
        
        self.rect.y += v_y(time, self.vertical_speed)
        
        # trump administration mexican border control
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.keep_moving = False
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.keep_moving = False
            # rah = v_x(time, self.horizontal_speed, True)
            # vx = rah[0]; self.keep_moving = rah[1]
            # if self.keep_moving is 0: self.keep_moving = False
            # self.rect.x += vx

class Star(pygame.sprite.Sprite):
    def __init__ (self):
        raise NotImplementedError
    def update(self):
        raise NotImplementedError

class Booster(pygame.sprite.Sprite):
    def __init__(self):
        raise NotImplementedError
    def update(self):
        raise NotImplementedError
    
class Fuel(pygame.sprite.Sprite):
    def __init__(self):
        raise NotImplementedError
    def update(self):
        raise NotImplementedError
    
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load() #still needs implementing!!
        self.surf.set_colorkey()
        self.rect = self.surf.get_rect(center = ())
        # self.speed = 

        raise NotImplementedError
    def update(self):
        raise NotImplementedError

# || ELEMENTS ||

main_plane = Plane()

plane_group = pygame.sprite.Group()
plane_group.add(main_plane)

# || GAME WINDOW ||

running = True
dt = 0

time = 0
while running:
    time += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(SKY_BLUE)

    #RENDER YOUR GAME HERE

    user_input = pygame.key.get_pressed()
    plane_group.update(time)
    plane_group.draw(window)

    pygame.display.flip()
    dt = clock.tick(FPS)/1000

#https://stackoverflow.com/questions/63350720/pygame-mouse-speed

# Clean up
pygame.quit()
sys.exit()
