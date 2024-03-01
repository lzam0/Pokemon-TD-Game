import pygame
import os
from .enemy import Enemy
#import enemy_sprites

imgs = []
for x in range(2):
    add_str = str(x)    
    imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assests/enemies", "lion_"+add_str+".png")),(64,64)))

class Lion(Enemy):

    def __init__(self):
        super().__init__()
        self.name = "Lion"
        self.health = 25
        self.max_health = self.health
        self.imgs = imgs[:]
        self.money = self.max_health
        #self.name = "bird" # different names so not sure what to use
