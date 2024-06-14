# || IMPORT STATEMENTS ||

import pygame, sys
from game_items import *
from pygame.locals import *
from random import randint, random

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
        if game_running:
            if event.type == ADD_FUEL:
                new_fuel = Fuel(all_speed, main_plane.rect.right)
                fuel_group.add(new_fuel)
            if event.type == ADD_BOOSTER:
                new_booster = Booster(all_speed, main_plane.rect.right)
                booster_group.add(new_booster)
            if event.type == ADD_CLOUD:
                new_cloud = Cloud(all_speed)
                cloud_group.add(new_cloud)

    if game_running:
        cloud_group.update()
        cloud_group.draw(window)
        plane_group.update(time, keyPressed)
        plane_group.draw(window)
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
            window.blit(Logo, (SCREEN_WIDTH/2-100,SCREEN_HEIGHT/2-100))
        else:
            # display stats from last run
            pass

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
