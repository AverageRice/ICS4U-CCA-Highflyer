# || IMPORT STATEMENTS ||

import pygame, sys
from pygame.locals import *
from random import randint, random

# || CONSTANTS ||

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1200
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
OFF_WHITE = (196, 196, 196)
GRAVITY_TIMER = 0

# || SPRITES GROUPS ||

plane_group = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
booster_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()

# || VELOCITY FUNCTIONS ||

def v_y(t, vy_o):
    global GRAVITY_TIMER
    '''projectile motion vertical velocity function for the plane'''
    return ((vy_o*GRAVITY_TIMER+0.0005*GRAVITY_TIMER**2)/100)

def v_x(t, vx_o):
    '''projectile motion horizontal velocity function for the plane'''
    final = vx_o
    return (final)

# || STATS MANAGEMENT FOR JUPYTER/STATISTIC PORTION ||

main_db = [] # contains player list containers. Each player container as follows: [max_range, max_height, gas_used, fuel_effeciency]

# || VARS ||

show_menu = True
game_running = False
first_run = True
show_instructions = False
show_upgrades_menu = False
all_speed = -4
cloud_spawn_rate = 1000

# || GAME OBJECTS ||
  
class Plane(pygame.sprite.Sprite):
    def __init__ (self, velocity_x = randint(0,0), velocity_y = randint(1,4)):
        pygame.sprite.Sprite.__init__(self)

        self.horizontal_speed = velocity_x
        self.vertical_speed = velocity_y

        self.image = pygame.image.load("paper_airplane.png")
        self.image = pygame.transform.scale(self.image, (75,75))

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 2)

        self.keep_moving = True
        self.gas = 100
        self.nitrous = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.boost_const = 2

        # Stats for pandas analysis
        self.final_range = 0
        self.max_height = 0
        self.gas_used = 0
        self.nitrous_used = 0
        self.fuel_effeciency = 0.25

    def update(self, time, keystatus):
        global show_menu, GRAVITY_TIMER, all_speed, game_running, cloud_spawn_rate

        if not game_running: return
        self.velocity_x = v_x(time, self.horizontal_speed)
        if self.keep_moving:
            self.rect.x += self.velocity_x
        
        self.velocity_y = v_y(time, self.vertical_speed)
        self.rect.y += self.velocity_y

        # update max height stat
        if self.rect.y > self.max_height:
            self.max_height == self.rect.bottom
        
        # trump administration mexican border control
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.keep_moving = False
        if self.rect.top < 0:
            self.rect.top = 0

        # If run end
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.keep_moving = False
            show_menu = True
            game_running = False
            all_speed = 0

            # update landing range stat
            self.final_range = self.rect.left
            # find amt of gas used in attempt
            self.gas_used = 100 - self.gas

            # save all to main_db
            run_data = [self.final_range, self.max_height, self.gas_used, self.fuel_effeciency, time]
            main_db.append(run_data)

            # clear powerup sprite groups
            booster_group.empty()
            fuel_group.empty()
            star_group.empty()
        
        # if holding space, boost up
        if keystatus[K_SPACE] == True: 
            if self.gas > 0:
                GRAVITY_TIMER = 20
            self.boost(time)

        # Collision detection with fuel objects
        fuel_collisions = pygame.sprite.spritecollide(self, fuel_group, True)
        for fuel in fuel_collisions:
            self.gas += 20
            fuel_group.remove(fuel)
        # Collision detection with booster objects
        booster_collisions = pygame.sprite.spritecollide(self, booster_group, True)
        for booster in booster_collisions:
            self.rect.x += 2.5*self.velocity_x # booster not working rn, fix later
            GRAVITY_TIMER = 0
            all_speed -= 3
            self.boost_const += 1.5
            cloud_spawn_rate += 800
            booster_group.remove(booster)
    
    def boost(self, time):
        time -= 1
        '''add some height to the plane as a userevent triggered boost by K_SPACE'''
        if self.gas <= 0: return
        if not self.keep_moving: return
        self.rect.y -= self.boost_const*self.velocity_y + 2
        self.gas -= self.fuel_effeciency

class Star(pygame.sprite.Sprite):
    def __init__ (self, spawn_x_range_start):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('star.png')
        self.image = pygame.transform.scale(self.image, (15,15))
        self.rect = self.image.get_rect(center = (randint(spawn_x_range_start,SCREEN_WIDTH+1000), randint(0, SCREEN_HEIGHT)))

    def update(self):
        self.rect = self.rect

class Booster(pygame.sprite.Sprite):
    def __init__(self, x_velocity, spawn_x_range_start):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('booster.png')
        self.image = pygame.transform.scale(self.image, (65,65))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH+1000, randint(0, SCREEN_HEIGHT)))
        self.x_velocity = x_velocity

    def update(self):
        self.rect.x += self.x_velocity
        if self.rect.right < 0:
            self.kill()
    
class Fuel(pygame.sprite.Sprite):
    def __init__(self, x_velocity, spawn_x_range_start):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('fuel.png')
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect(center = (SCREEN_WIDTH+1000, randint(0, SCREEN_HEIGHT)))
        self.x_velocity = x_velocity

    def update(self):
        self.rect.x += self.x_velocity
        if self.rect.right < 0:
            self.kill()
    
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x_velocity, x = randint(SCREEN_WIDTH, SCREEN_WIDTH*2), y = None):
        pygame.sprite.Sprite.__init__(self)
        self.v_x = x_velocity
        self.image = pygame.image.load('cloud_medium.png')
        self.size = randint(100,250)
        self.image = pygame.transform.scale(self.image, (self.size,self.size))
        if not y:
            y = randint(0, SCREEN_HEIGHT-130)
        self.rect = self.image.get_rect(center = (x, y))
        
    def update(self):
        self.rect.x += self.v_x
        if self.rect.right < 0:
            self.kill()