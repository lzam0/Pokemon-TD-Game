import pygame
import os
from .tower import Tower
from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "menu.png")), (175, 250))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "upgrade.png")), (50, 50))

# load Turtle images
tower_imgs = []
for x in range(5):
	add_str = str(x)
	tower_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assests/tower/base", "turtle_"+add_str+".png")),(64,64)))

class TurtleTower(Tower):
	
	def __init__(self, x, y):
		super().__init__(x , y)
		self.name = "Turtwig"
		self.range = 150
		self.damage = 4
		self.att_speed = 0.4
		self.tower_imgs = tower_imgs[:2]

		self.menu = Menu(self, 25, 300, menu_bg, [200,800, 1200, 3300, "FULLY EVOLVED"]) # buy price | 2nd upgrade | max upgrade
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
					self.name = "Grotle"
				elif self.level == 3:
					self.name = "Torterra"
				# Ensure tower image is reset to the first image after upgrade
				self.tower_count = 0
