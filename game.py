import pygame
import os
import sys
import datetime
import random
import time

# setings
from settings import *

# Enemies
from enemies.bird import Bird
from enemies.lion import Lion
from enemies.flower import Flower

# Towers
from towers import *
from towers.monkey import MonkeyTower
from towers.turtle import TurtleTower
from towers.penguin import PenguinTower

from menu.menu import VerticalMenu

# Tower Name
tower_name = ["Monkey", "Penguin", "Turtle"]

# Game Atribute Images
lives_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "heart.png")), (50, 50))
money_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "pokecash.png")), (50, 50))

# Vertical Buy Menu
vert_menu = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "menu.png")), (150, 350))

# Tower Buy Images
monkey = pygame.transform.scale(pygame.image.load(os.path.join("game_assests/tower/icon", "monkey.png")),(64,64))
penguin = pygame.transform.scale(pygame.image.load(os.path.join("game_assests/tower/icon", "penguin.png")),(64,64))
turtle = pygame.transform.scale(pygame.image.load(os.path.join("game_assests/tower/icon", "turtle.png")),(64,64))



from pygame import display

pygame.init()
pygame.font.init()


waves = []

def wave_gen():
    # using geometic sequence
    # 10
    for i in range(11):
        a = 5
        d = 5
        enemy = a+(i-1)*d
        waves.append([enemy,0,0])

    # 20
    for i in range(1,11):
        a = 1
        d = 1
        enemy = a+(i-1)*d
        waves.append([0,enemy,0])

    # 30
    for i in range(2,12):
        a = 0
        d = 5
        enemy = a + (i - 1) * d

        A = 1
        D = 5
        enemy_2 = A = (i-1)*D

        waves.append([enemy, enemy_2, 0])

    # first boss wave round on wave 30
    waves.append([0,0,1]) # Boss Round

    for i in range(8):
        a = 70
        d = 5

        enemy = a+(i-1)*d
        waves.append([enemy, enemy, 0])
wave_gen()

class Game:
    def __init__(self):
        # Window Title
        pygame.display.set_caption(TITLE)

        # Window Screen
        self.width = WIDTH
        self.height = HEIGHT
        self.win = pygame.display.set_mode((self.width, self.height))

        # Sprites
        self.enemys = []
        self.towers = []

        # Game Attributes
        self.lives = 100
        self.money = 1000

        # Background
        self.img = pygame.image.load(os.path.join("game_assests","bg.png"))
        self.bg = pygame.transform.scale(self.img, (self.width, self.height)) # change this for actual bg
        self.clicks = [] # used to get positions of the enemy pathway

        # Menu
        self.timer = time.time()
        self.pause = True
        self.selected_tower = None

        # Vertical Menu
        self.menu = VerticalMenu(1060 , 350,vert_menu)
        self.menu.add_btn(monkey, "Monkey", 500)
        self.menu.add_btn(penguin, "Penguin", 500)
        self.menu.add_btn(turtle, "Turtle", 500)
        self.moving_object = None

        # Waves
        self.wave = 0
        self.current_wave = waves[self.wave][:]

        # Fonts
        self.font = pygame.font.SysFont("Helvetica", 40)

    def gen_enemies(self):
        if sum(self.current_wave) == 0:
            if len(self.enemys) == 0:
                self.wave += 1
                self.current_wave = waves[self.wave]
                self.pause = True
        else:
            wave_enemies = [Bird(), Lion(), Flower()]
            for x in range(len(self.current_wave)):
                if self.current_wave[x] != 0:
                    self.enemys.append(wave_enemies[x])
                    self.current_wave[x] = self.current_wave[x] - 1
                    break

    def run(self):
        fps = pygame.time.Clock()
        run = True
        while run:
            fps.tick(FPS)  # frame rate

            # Generate Enemies
            if self.pause != False:
                spawn_time = random.uniform(0.75, 5)
                if time.time() - self.timer >= spawn_time:
                    self.timer = time.time()
                    self.gen_enemies()

            # Coordinate generator
            pos = pygame.mouse.get_pos()

            # Check For moving Object
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])

            # Event Handler 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If Moving an object and click
                    if self.moving_object:
                        if self.moving_object.name in tower_name:
                            self.towers.append(self.moving_object)


                        self.moving_object.moving = False
                        self.moving_object = None

                    else:
                        # Clicked on Buy Menu
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                print(side_menu_button, "purchased")
                                self.add_tower(side_menu_button)


                        # Clicked on Tower
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    print("Upgrade Cost",cost)
                                    if self.money >= cost:
                                        self.money -= cost # fix get upgrade cost method
                                        print("Tower Upgraded | Level:", self.selected_tower.level)
                                        self.selected_tower.upgrade()

                            if not(btn_clicked):
                                for tw in self.towers:
                                    if tw.click(pos[0], pos[1]):
                                        tw.selected = True
                                        self.selected_tower = tw
                                    else:
                                        tw.selected = False

                        # tower clicked
                        for tw in self.towers:
                            if tw.click(pos[0], pos[1]):
                                tw.selected = True
                                self.selected_tower = tw
                                print("Tower", self.selected_tower.name, "is selected  ")
                            else:
                                tw.selected = False

                # Pause Game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    while True: #Infinite loop that will be broken when the user press the space bar again
                        event = pygame.event.wait()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            break

                # Loop through enemies
                to_del = []
                for en in self.enemys:
                    en.move()
                    if en.y < -25:
                        to_del.append(en)

                # delete all enemies off screen
                for d in to_del:
                    self.lives -= 1
                    self.enemys.remove(d)

                # Lose
                if self.lives <= 0:
                    print("You Lose")
                    run = False

            self.draw()

            pygame.display.update()

        pygame.quit()
    
    def draw(self):
        self.win.blit(self.bg, (0,0)) # BG
        
        #Used to get the position for enemy pathway
        for p in self.clicks:
             pygame.draw.circle(self.win, (255,0,0), (p[0], p[1]), 5, 0)
    
        # draw enemy
        for en in self.enemys:
            en.draw(self.win)

        # draw towers
        for tw in self.towers:
            tw.draw(self.win)

        # monkey increase when enemy killed
        for tw in self.towers:
            self.money += tw.attack(self.enemys)

        # draw moving obj
        if self.moving_object:
            self.moving_object.draw(self.win)

        # used to get the position for enemy pathway
        for p in self.clicks:
             pygame.draw.circle(self.win, (255,0,0), (p[0], p[1]), 5, 0)

        # draw vertical menu
        self.menu.draw(self.win)

        # draw lives
        life_txt = self.font.render(str(self.lives), 1, WHITE)
        self.win.blit(lives_img, (10, 10))  # image
        self.win.blit(life_txt, (75, 10)) # text

        # draw cash
        money_txt = self.font.render(str(self.money), 1, WHITE)
        self.win.blit(money_img, (10, 75))  # image
        self.win.blit(money_txt, (75, 75)) # text

        # draw wave
        wave_text = self.font.render("Wave:" + str(self.wave), 1, WHITE)
        self.win.blit(wave_text, (15, 625))  # text

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["Monkey", "Penguin", "Turtle"]
        object_list = [MonkeyTower(x,y), PenguinTower(x,y), TurtleTower(x,y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "NOT VALID NAME")

game = Game()
game.run()
