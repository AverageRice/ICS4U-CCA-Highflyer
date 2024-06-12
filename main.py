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

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 2)

        self.keep_moving = True
        self.gas = 100
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self, time, keystatus):
        self.velocity_x = v_x(time, self.horizontal_speed)
        if self.keep_moving:
            self.rect.x += self.velocity_x
        
        self.velocity_y = v_y(time, self.vertical_speed)
        self.rect.y += self.velocity_y
        
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
        
        # if holding space, boost up
        if keystatus[K_SPACE] == True: self.boost(time)
        # if holding right arrow, speed up
        if keystatus[K_RIGHT] == True: self.speed_up(time)
    
    def boost(self, time):
        '''add some height to the plane as a userevent triggered boost'''
        if self.gas <= 0: return
        if not self.keep_moving: return
        self.rect.y -= 1.6*self.velocity_y
        self.gas -= 0.25
    
    def speed_up(self, time):
        '''convert some of the plane's vertical velocity into horizontal velocity'''
        if not self.keep_moving: return
        self.rect.x += 1.6*self.velocity_x
        self.rect.y += 1.6*self.velocity_y

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
        #self.surf = pygame.image.load() #still needs implementing!!
        self.surf.set_colorkey(WHITE, RLEACCEL)
        self.rect = self.surf.get_rect(center = (SCREEN_WIDTH,
                                           randint(0, SCREEN_HEIGHT))) #spawn anywhere in the game environment
        
    def update(self):
        #only remove once they move off-screen TO THE LEFT!!!

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

    keyPressed = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
                # main_plane.boost() # not used bc implementing keyholds in

    window.fill(SKY_BLUE)

    #RENDER YOUR GAME HERE

    user_input = pygame.key.get_pressed()
    plane_group.update(time, keyPressed)
    plane_group.draw(window)

    pygame.display.flip()
    dt = clock.tick(FPS)/1000

# https://stackoverflow.com/questions/63350720/pygame-mouse-speed

# Clean up
pygame.quit()
sys.exit()
