import pygame
import os
from .enemy import Enemy

imgs = []
for x in range(2):
    add_str = str(x)    
    imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assets/enemies", "flower_"+add_str+".png")),(64,64)))

class Flower(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "Flower"
        self.health = 50
        self.max_health = self.health
        self.imgs = imgs[:]
        self.money = self.max_health
        #self.name = "bird" # different names so not sure what to use
