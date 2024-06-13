# || IMPORT STATEMENTS ||

import pygame, sys
from pygame.locals import *
from random import randint, random

# || CONSTANTS ||

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1850
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
OFF_WHITE = (196, 196, 196)
GRAVITY_TIMER = 0

# || PYGAME SETUP ||

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# || BOOLEANS ||

show_menu = True
game_running = False
first_run = True
show_instructions = False
show_upgrades_menu = False

# || STATS MANAGEMENT FOR JUPYTER/STATISTIC PORTION ||

main_db = [] # contains player list containers. Each player container as follows: [max_range, max_height, gas_used, fuel_effeciency]

# || CLASSES ||

#functionality:
#mathematics determine position of paper airplane after thrown

def v_y(t, vy_o):
    global GRAVITY_TIMER
    '''projectile motion vertical velocity function for the plane'''
    return ((vy_o*GRAVITY_TIMER+0.2*GRAVITY_TIMER**2)/100)

def v_x(t, vx_o):
    '''projectile motion horizontal velocity function for the plane'''
    final = vx_o
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
        self.gas = 100 #TEMPORARY 
        self.velocity_x = 0
        self.velocity_y = 0

        # Stats for pandas analysis
        self.final_range = 0
        self.max_height = 0
        self.gas_used = 0
        self.fuel_effeciency = 1.25

    def update(self, time, keystatus):
        global show_menu, GRAVITY_TIMER

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

            # save all to main_db
            run_data = [self.final_range, self.max_height, self.gas_used, self.fuel_effeciency, time]
            main_db.append(run_data)
        
        # if holding space, boost up
        if keystatus[K_SPACE] == True: 
            if self.gas > 0:
                GRAVITY_TIMER = 20
            self.boost(time)
        # if holding right arrow, speed up
        if keystatus[K_RIGHT] == True: self.speed_up(time)

        # Collision detection with fuel objects
        fuel_collisions = pygame.sprite.spritecollide(self, fuel_group, True)
        for fuel in fuel_collisions:
            self.gas += 30
            fuel_group.remove(fuel)
        # Collision detection with booster objects
        booster_collisions = pygame.sprite.spritecollide(self, booster_group, True)
        for booster in booster_collisions:
            self.rect.x += 1.6*self.velocity_x
            GRAVITY_TIMER = 0
            booster_group.remove(booster)
    
    def boost(self, time):
        time -= 1
        '''add some height to the plane as a userevent triggered boost'''
        if self.gas <= 0: return
        if not self.keep_moving: return
        self.rect.y -= 2*self.velocity_y
        self.gas -= self.fuel_effeciency
    
    def speed_up(self, time):
        '''convert some of the plane's vertical velocity into horizontal velocity'''
        if not self.keep_moving: return
        self.rect.x += 1.6*self.velocity_x
        self.rect.y += 1.6*self.velocity_y

class Star(pygame.sprite.Sprite):
    def __init__ (self, spawn_x_range_start):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('star.png')
        self.image = pygame.transform.scale(self.image, (15,15))
        self.rect = self.image.get_rect(center = (randint(spawn_x_range_start,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))

    def update(self):
        self.rect = self.rect

class Booster(pygame.sprite.Sprite):
    def __init__(self, x_velocity, spawn_x_range_start):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('booster.png')
        self.image = pygame.transform.scale(self.image, (65,65))
        self.rect = self.image.get_rect(center = (randint(spawn_x_range_start,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))
        self.x_velocity = x_velocity

    def update(self):
        self.rect.x += self.x_velocity
    
class Fuel(pygame.sprite.Sprite):
    def __init__(self, x_velocity, spawn_x_range_start):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('fuel.png')
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect(center = (randint(spawn_x_range_start,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT)))
        self.x_velocity = x_velocity

    def update(self):
        self.rect.x += self.x_velocity
    
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x_velocity):
        pygame.sprite.Sprite.__init__(self)
        self.v_x = x_velocity/4
        self.image = pygame.image.load('cloud_medium.png')
        self.image = pygame.transform.scale(self.image, (125,125))
        #self.image.fill(OFF_WHITE)
        self.rect = self.image.get_rect(center = (randint(0,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))) #spawn anywhere in the game environment (randint(0,SCREEN_WIDTH), randint(0, SCREEN_HEIGHT))
        
    def update(self):
        self.rect.x += self.v_x
        #if self.rect.left > SCREEN_WIDTH:
            #self.kill
        #only remove once they move off-screen TO THE LEFT!!!

# || EVENTS ||

ADD_CLOUD = pygame.USEREVENT + 12
pygame.time.set_timer(ADD_CLOUD, 1200)
# 2 args [what to happen, how often]

ADD_FUEL = pygame.USEREVENT + 13
pygame.time.set_timer(ADD_FUEL, 3000)

Add_BOOSTER = pygame.USEREVENT + 14
pygame.time.set_timer(Add_BOOSTER, 3000)

# || ELEMENTS ||

# || TEXT/MENU ELEMENTS ||

game_instructions = ["INSTRUCTIONS", "Press [SPACE] to boost up", "Press [RIGHT ARROW] to speed up"]
upgrades_menu = ["UPGRADES", "1. Fuel Efficiency + 10%", "More in future versions", "Upon further investment"]

font = pygame.font.Font('Toyota-Type.ttf', 36)
font_small = pygame.font.Font('Toyota-Type.ttf', 24)

A_Start_Game = font.render('[1] Start Game', True, (255, 255, 255))
B_Instructions_Button = font.render('[2] Instructions', True, (255, 255, 255))
C_Upgrades_Button = font.render('[3] Upgrades', True, (255, 255, 255))
D_Save_and_Quit = font.render('[4] Save and Quit', True, (255, 255, 255))

Logo = pygame.image.load('highflyer logo.png')
Logo = pygame.transform.scale(Logo, (3774/5,2391/5))

# || SPRITE GROUPS ||

main_plane = Plane()

plane_group = pygame.sprite.Group()
plane_group.add(main_plane)

cloud_group = pygame.sprite.Group()
booster_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()

# || GAME WINDOW/LOOP ||

running = True
dt = 0

runs = 0
time = 0
while running:
    if running == False:
        break

    # || DEBUG INFO ||

    # print(main_plane.velocity_y)

    # || TIME UPDATING ||

    time += 1

    if game_running: 
        GRAVITY_TIMER += 1 

    keyPressed = pygame.key.get_pressed()

    window.fill(SKY_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                GRAVITY_TIMER = 0 
                runs += 1
                A_Start_Game = font.render('[1] Play Again', True, (255, 255, 255))
                time = 0
                main_plane = Plane()
                plane_group.empty()
                plane_group.add(main_plane)
                game_running = True
                show_menu = False
                show_instructions = False
                cloud_group.empty()
                booster_group.empty()
                fuel_group.empty()
                star_group.empty()
                # save main_db to a a CSV file and clear the main_db container for next iteration
                if first_run:
                    first_run = False
            if event.key == pygame.K_2:
                show_instructions = not show_instructions
            if event.key == pygame.K_3:
                show_upgrades_menu = not show_upgrades_menu
            if event.key == pygame.K_4:
                # save main_db to a a CSV file and quit the pygame window
                pygame.quit()
                running = False
                break
        if event.type == ADD_CLOUD:
            new_cloud = Cloud(0)
            cloud_group.add(new_cloud)
        if event.type == ADD_FUEL:
            new_fuel = Fuel(0)
            print('fuel added')
            fuel_group.add(new_fuel)
        if event.type == Add_BOOSTER:
            new_booster = Booster(0)
            print('booster added')
            booster_group.add(new_booster)

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
    
    # break the game loop if the player save and quit
    if not running:
        break

    if show_menu:
        time -= 1
        window.blit(A_Start_Game, (20, 10))
        window.blit(B_Instructions_Button, (20, 50))
        window.blit(C_Upgrades_Button, (20, 90))
        window.blit(D_Save_and_Quit, (20, 130))
        if first_run:
            window.blit(Logo, (800,10))

    if not show_menu:
        gas_level_indicator = font.render('Fuel Remaining: ' + str(main_plane.gas) + '%', True, (255, 255, 255))
        window.blit(gas_level_indicator, (20, 420))
        runs_indicator = font.render('Runs: ' + str(runs), True, (255, 255, 255))
        window.blit(runs_indicator, (20, 380))

    # || DISPLAY AND UPDATE ELEMENTS ||

    if game_running:
        plane_group.update(time, keyPressed)
        plane_group.draw(window)
        cloud_group.update()
        cloud_group.draw(window)
        booster_group.update()
        booster_group.draw(window)
        fuel_group.update()
        fuel_group.draw(window)
        star_group.update()
        star_group.draw(window)

    pygame.display.flip()
    dt = clock.tick(FPS)/1000

# || STATS MANAGEMENT FOR JUPYTER/STATISTIC PORTION ||

# remove duplicate entries in main_db
DB = []
for i in range(len(main_db)):
    if main_db[i] not in DB:
        DB.append(main_db[i])
# save main_db to a CSV file
with open('data.csv', 'w') as f:
    for i in range(len(DB)):
        write = str(DB[i])
        f.write(write[1:-1] + '\n')
# Clean up

# || ENDING PROGRAM ||

pygame.quit()
sys.exit()
