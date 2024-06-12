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
OFF_WHITE = (196, 196, 196)

# || PYGAME SETUP ||

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# basics lmao

show_menu = True
game_running = False
first_run = True
show_instructions = False
show_upgrades_menu = False

# stat management

main_db = [] # contains player list containers. Each player container as follows: [max_range, max_height, gas_used, fuel_effeciency]

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
        self.image = pygame.image.load("paper_airplane.png")
        self.image = pygame.transform.scale(self.image, (75,75))
        # self.image = pygame.Surface((25,25)) #to be replaced
        # self.image.fill(WHITE) #to be replaced

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 8, SCREEN_HEIGHT / 2)

        self.keep_moving = True
        self.gas = 100
        self.velocity_x = 0
        self.velocity_y = 0

        # Stats for pandas analysis
        self.final_range = 0
        self.max_height = 0
        self.gas_used = 0
        self.fuel_effeciency = 1.25

    def update(self, time, keystatus):
        global show_menu

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
        # If game end
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.keep_moving = False
            show_menu = True
            # update landing range stat
            self.final_range = self.rect.left
            # find amt of gas used in attempt
            self.gas_used = 100 - self.gas

            # useless non working garbage code!
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
        self.gas -= self.fuel_effeciency
    
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
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('cloud_medium.png')
        self.image = pygame.transform.scale(self.image, (25,25))
        #self.image.fill(OFF_WHITE)
        self.rect = self.image.get_rect(center = (randint(0,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))) #spawn anywhere in the game environment (randint(0,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
        
    def update(self):
        pass
        #if self.rect.left > SCREEN_WIDTH:
            #self.kill
        #only remove once they move off-screen TO THE LEFT!!!

# || EVENTS ||

ADD_CLOUD = pygame.USEREVENT + 12
pygame.time.set_timer(ADD_CLOUD, 10000)
# 2 args [what to happen, how often]

# || ELEMENTS ||

game_instructions = ["INSTRUCTIONS", "Press [SPACE] to boost up", "Press [RIGHT ARROW] to speed up"]
upgrades_menu = ["UPGRADES", "1. Fuel Efficiency + 10%", "More in future versions", "Upon further investment"]

font = pygame.font.Font('Toyota-Type.ttf', 36)
font_small = pygame.font.Font('Toyota-Type.ttf', 24)

main_plane = Plane()
A_Start_Game = font.render('[A] Start Game', True, (255, 255, 255))
B_Instructions_Button = font.render('[B] Instructions', True, (255, 255, 255))
C_Upgrades_Button = font.render('[C] Upgrades', True, (255, 255, 255))

all_sprites_group = pygame.sprite.Group()
all_sprites_group.add(main_plane)

cloud_group = pygame.sprite.Group()

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
            if event.key == pygame.K_a:
                A_Start_Game = font.render('[A] Play Again', True, (255, 255, 255))
                time = 0
                main_plane = Plane()
                all_sprites_group.empty()
                all_sprites_group.add(main_plane)
                game_running = True
                show_menu = False
                show_instructions = False
            if event.key == pygame.K_b:
                show_instructions = not show_instructions
            if event.key == pygame.K_c:
                show_upgrades_menu = not show_upgrades_menu

        if event.type == ADD_CLOUD:
            new_cloud = Cloud()
            cloud_group.add(new_cloud)

    window.fill(SKY_BLUE)

    # Texts to display
    gas_level_indicator = font.render('Fuel Remaining: ' + str(main_plane.gas) + '%', True, (255, 255, 255))
    window.blit(gas_level_indicator, (20, 420))
    if show_instructions:
        for i in range(len(game_instructions)):
            instruction = font_small.render(game_instructions[i], True, (255, 255, 255))
            window.blit(instruction, (SCREEN_WIDTH / 2 - 170, 160 + 30*i))
    if show_upgrades_menu:
        for i in range(len(upgrades_menu)):
            upgrade = font_small.render(upgrades_menu[i], True, (255, 255, 255))
            window.blit(upgrade, (SCREEN_WIDTH / 2 - 170, 160 + 30*i))
        # check for event to upgrade fuel efficiency
        if keyPressed[K_1]:
            main_plane.fuel_effeciency -= 0.1
            show_upgrades_menu = False

    #RENDER YOUR GAME HERE
    if show_menu:
        time -= 1
        window.blit(A_Start_Game, (20, 10))
        window.blit(B_Instructions_Button, (20, 50))
        window.blit(C_Upgrades_Button, (20, 90))
    
    user_input = pygame.key.get_pressed()
    if game_running:
        all_sprites_group.update(time, keyPressed)
        all_sprites_group.draw(window)

    pygame.display.flip()
    dt = clock.tick(FPS)/1000

# Clean up
pygame.quit()
sys.exit()
