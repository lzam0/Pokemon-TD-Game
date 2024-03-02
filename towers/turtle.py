import pygame
import os
from .tower import Tower
from menu.menu import Menu

# Load Turtle images
tower_imgs = []
for x in range(6):
    add_str = str(x)
    img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets/tower/base", "turtle_" + add_str + ".png")),(64,64))
    tower_imgs.append(img)

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu.png")), (175, 250))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upgrade.png")), (50, 50))

class TurtleTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.name = "Turtwig"
        self.range = 150
        self.damage = 4
        self.att_speed = 0.4
        # Set tower images based on the current level
        self.tower_imgs = tower_imgs[:2]  # Initial tower images (Turtwig)
        self.menu = Menu(self, 25, 300, menu_bg, [600, 1700, "FULLY EVOLVED"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

    def upgrade(self):
        if self.level < 3:  # Allow three upgrades (Turtwig -> Grotle -> Torterra)
            self.level += 1
            # Double the damage with each upgrade
            self.damage *= 2
            # Set tower images based on the current level
            start_index = (self.level - 1) * 2  # Each level has two images
            end_index = start_index + 2
            self.tower_imgs = tower_imgs[start_index:end_index]
            # Update tower name based on the current level
            if self.level == 2:
                self.name = "Grotle"
            elif self.level == 3:
                self.name = "Torterra"
            # Ensure tower image is reset to the first image after upgrade
            self.tower_count = 0

    def get_upgrade_cost(self):
        return self.menu.get_item_cost()