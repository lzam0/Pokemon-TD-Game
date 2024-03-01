import pygame
import os
from .enemy import Enemy
#import enemy_sprites

imgs = []
for x in range(2):
    add_str = str(x)    
    imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assests/enemies", "bird_"+add_str+".png")),(64,64)))

class Bird(Enemy):

    def __init__(self):
        super().__init__()
        self.name = "Bird"
        self.health = 10
        self.max_health = self.health
        self.imgs = imgs[:]
        self.money = 10
