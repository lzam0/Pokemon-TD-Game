import pygame
import os
from .tower import Tower
from menu.menu import Menu

# Load all monkey images at once
tower_imgs = []
for i in range(6):
    add_str = str(i)
    tower_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assests/tower/base", "monkey_" + add_str + ".png")),(64, 64)))

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "menu.png")), (175, 250))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "upgrade.png")), (50, 50))

class MonkeyTower(Tower):
    
    def __init__(self, x, y):
        super().__init__(x, y)

        self.name = "Chimchar"
        self.range = 100
        self.damage = 7
        self.att_speed = 1
        self.tower_imgs = tower_imgs[:2]  # Set initial tower images to monkey_0 and monkey_1

        # Money
        self.menu = Menu(self, 25, 300, menu_bg, [1400, 2600, "FULLY EVOLVED"])  # Buy price | 2nd upgrade | max upgrade
        self.menu.add_btn(upgrade_btn, "Upgrade")

    def upgrade(self):
        if self.level < 2:  # Allow two upgrades
            self.level += 1
            self.damage *= 2  # Double the damage
            # Set tower images based on the current level
            start_index = (self.level - 1) * 2
            end_index = start_index + 2
            self.tower_imgs = tower_imgs[start_index:end_index]
            # Update tower name based on the current level
            if self.level == 2:
                self.name = "Monferno"
            elif self.level == 3:
                self.name = "Infernape"
            # Ensure tower image is reset to the first image after upgrade
            self.tower_count = 0

    def get_upgrade_cost(self):
        return self.menu.get_item_cost()