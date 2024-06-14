# || IMPORT STATEMENTS ||

import pygame, sys
from pygame.locals import *
from random import randint

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
        self.rect.center = (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2)

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

    def update(self, time, keystatus, running):
        global show_menu, all_speed, game_running, cloud_spawn_rate, GRAVITY_TIMER

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
        if keystatus[K_SPACE]:
            if self.gas > 0: GRAVITY_TIMER = 20
            self.boost(time)

        # Collision detection with fuel objects
        fuel_collisions = pygame.sprite.spritecollide(self, fuel_group, True)
        for fuel in fuel_collisions:
            self.gas += 20
            fuel_group.remove(fuel)
        # Collision detection with booster objects
        booster_collisions = pygame.sprite.spritecollide(self, booster_group, True)
        for booster in booster_collisions:
            # self.rect.x += 2.5*self.velocity_x # booster not working rn, fix later
            GRAVITY_TIMER = 0
            all_speed -= 3
            self.boost_const += 1.5
            cloud_spawn_rate += 1000
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
    def __init__(self, x_velocity):
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
    def __init__(self, x_velocity):
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
        
    def update(self, is_running = True):
        if not is_running: return
        self.rect.x += self.v_x
        if self.rect.right < 0:
            self.kill()

# || PYGAME SETUP ||

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# || EVENTS ||

ADD_FUEL = pygame.USEREVENT + 13
pygame.time.set_timer(ADD_FUEL, 5000)

ADD_BOOSTER = pygame.USEREVENT + 14
pygame.time.set_timer(ADD_BOOSTER, 3000)

ADD_CLOUD = pygame.USEREVENT + 15
pygame.time.set_timer(ADD_CLOUD, 1000)

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
Logo = pygame.transform.scale(Logo, (3774/8,2391/8))

# || Main Plane ||

main_plane = Plane()
plane_group.add(main_plane)

# || GAME WINDOW/LOOP ||

running = True
dt = 0

runs = 0
time = 0 # unit: screen refreshes
while running:
    if running == False:
        break

    # || TIME UPDATING ||

    time += 1

    if game_running: 
        GRAVITY_TIMER += 1 

    keyPressed = pygame.key.get_pressed()

    window.fill(SKY_BLUE)

    cloud_group.update(game_running)
    cloud_group.draw(window)
    plane_group.update(time, keyPressed, game_running)
    plane_group.draw(window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                # reset game physics
                GRAVITY_TIMER = 0 
                # change menu start text
                A_Start_Game = font.render('[1] Play Again', True, (255, 255, 255))
                # reset game logic bools
                all_speed = -4
                time = 0
                runs += 1
                game_running = True
                show_menu = False
                show_instructions = False
                # clear all sprite groups
                plane_group.empty()
                cloud_group.empty()
                # add new plane for next run
                main_plane = Plane()
                plane_group.add(main_plane)
                # create initial on-screen clouds
                for x in range(0,3):
                    new_cloud = Cloud(all_speed, randint(0, SCREEN_WIDTH))
                    cloud_group.add(new_cloud)
                # indicate first run completed
                if first_run: first_run = False
            if event.key == pygame.K_2:
                show_instructions = not show_instructions
            if event.key == pygame.K_3:
                show_upgrades_menu = not show_upgrades_menu
            if event.key == pygame.K_4:
                # quit pygame window
                pygame.quit()
                running = False
                break
        if game_running:
            if event.type == ADD_FUEL:
                new_fuel = Fuel(all_speed)
                fuel_group.add(new_fuel)
            if event.type == ADD_BOOSTER:
                new_booster = Booster(all_speed)
                booster_group.add(new_booster)
            if event.type == ADD_CLOUD:
                new_cloud = Cloud(all_speed)
                cloud_group.add(new_cloud)

    # break the game loop if the player save and quit
    if not running: 
        break

    if game_running:
        booster_group.update()
        booster_group.draw(window)
        fuel_group.update()
        fuel_group.draw(window)
        star_group.update()
        star_group.draw(window)
        
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

    if show_menu:
        time -= 1
        window.blit(A_Start_Game, (20, 10))
        window.blit(B_Instructions_Button, (20, 50))
        window.blit(C_Upgrades_Button, (20, 90))
        window.blit(D_Save_and_Quit, (20, 130))
        if first_run:
            window.blit(Logo, (SCREEN_WIDTH/2-100,SCREEN_HEIGHT/2-100))
        else:
            # display stats from last run
            Last_Run = font.render('Last Run Stats:', True, (255, 255, 255))
            window.blit(Last_Run, (20, 280))
            final_range = font.render('Final Range: ' + str(main_plane.final_range) + 'm', True, (255, 255, 255))
            window.blit(final_range, (20, 320))
            max_height = font.render('Max Height: ' + str(main_plane.max_height) + 'm', True, (255, 255, 255))
            window.blit(max_height, (20, 360))
            gas_used = font.render('Gas Used: ' + str(main_plane.gas_used) + '%', True, (255, 255, 255))
            window.blit(gas_used, (20, 400))
            # fuel_effeciency = font.render('Fuel Efficiency: ' + str(main_plane.fuel_effeciency) + '%', True, (255, 255, 255))
            # window.blit(fuel_effeciency, (20, 320))
            time_elapsed = font.render('Time Elapsed: ' + str(time) + 'units', True, (255, 255, 255))
            window.blit(time_elapsed, (20, 440))

    if not show_menu:
        gas_level_indicator = font.render('Fuel Remaining: ' + str(main_plane.gas) + '%', True, (255, 255, 255))
        window.blit(gas_level_indicator, (20, 410))
        nitrous_level_indicator = font.render('Nitrous Remaining: ' + str(main_plane.nitrous) + '%', True, (255, 255, 255))
        window.blit(nitrous_level_indicator, (20, 450))
        runs_indicator = font.render('Runs: ' + str(runs), True, (255, 255, 255))
        window.blit(runs_indicator, (20, 370))

    pygame.display.flip()
    dt = clock.tick(FPS)/1750

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
