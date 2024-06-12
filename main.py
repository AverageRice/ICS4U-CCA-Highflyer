# || IMPORT STATEMENTS ||

import pygame, sys
from pygame.locals import *

# || CONSTANTS ||

SCREEN_HEIGHT = 690
SCREEN_WIDTH = 1100
FPS = 30

GRAVITY = 9.8

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

def distance(velocity_x,time):
    

class Plane(pygame.sprite.Sprite):
    def __init__ (self, velocity_x, velocity_y):
        #SPEEDS
        self.horizontal_speed = velocity_x
        self.vertical_speed = velocity_y

        #self.image = pygame.image.load("plane.png").convert()
        self.surface = pygame.Surface((25,25)) #to be replaced
        self.surface.fill(WHITE) #to be replaced
        
        #self.rect = self.image.get_rect()
        self.rect = self.surface.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        position_x = distance(velocity_x,)
        position_x = self.horizontal_speed*time #need to begin tracking time immediatley after plane is thrown.
        position_y = 

        return position_x

    def update(self):
        if user_input[K_SPACE]:
            self.horizontal_speed += 10
            self.vertical_speed += 10
            self.fuel

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

main_plane = Plane(2,3)

# || GAME WINDOW ||

running = True
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(SKY_BLUE)

    #RENDER YOUR GAME HERE

    user_input = pygame.key.get_pressed()
    main_plane.update()

    pygame.display.flip()
    dt = clock.tick(FPS)/1000

pygame.quit()

#https://stackoverflow.com/questions/63350720/pygame-mouse-speed
