import pygame
import os
from .tower import Tower
from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "menu.png")), (175, 250))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "upgrade.png")), (50, 50))

# load monkey images according to tower level + different dmg and names
tower_imgs = []
for i in range(5):
	add_str = str(i)
	tower_imgs.append(pygame.transform.scale(pygame.image.load(os.path.join("game_assests/tower/base", "monkey_"+add_str+".png")),(64,64)))

class MonkeyTower(Tower):
	
	def __init__(self, x, y):
		super().__init__(x , y)

		self.name = "Monkey"
		self.range = 100
		self.damage = 7
		self.att_speed = 1
		self.tower_imgs = tower_imgs[:]

		# money
		self.menu = Menu(self, 25, 300, menu_bg, [600, 1500, 3800, "FULLY EVOLVED"])  # buy price | 2nd upgrade | max upgrade
		self.menu.add_btn(upgrade_btn, "Upgrade")