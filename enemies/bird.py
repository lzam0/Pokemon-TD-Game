import pygame
import os
from .enemy import Enemy
#import enemy_sprites

# Preload images
bird_imgs = [pygame.transform.scale(pygame.image.load(os.path.join("game_assets/enemies", f"bird_{x}.png")),(64,64)) for x in range(2)]

class Bird(Enemy):
    # Class attribute for images
    imgs = bird_imgs

    def __init__(self):
        super().__init__()
        self.name = "Starely"
        self.health = 10
        self.max_health = self.health
        # Reuse class attribute instead of creating a copy
        self.imgs = Bird.imgs[:]
        self.money = 10


# I want to add more bird enemies (the evoluitions of starley)