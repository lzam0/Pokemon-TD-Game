import pygame, os
from settings import *

pokecash = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "pokecash.png")), (50, 50))
buy_pokecash = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "pokecash.png")), (25, 25))

class Button:
	def __init__(self, menu, img, name):
		self.name = name

		self.img = img

		self.x = menu.x
		self.y = menu.y

		self.width = self.img.get_width()
		self.height = self.img.get_height()

		self.menu = menu

	def click(self, X, Y):
		if X <= self.x + self.width and X >= self.x:
			if Y <= self.y + self.height and Y >= self.y:
				return True
		return False

	def tower_draw(self,win): # Draw Tower BTN Image
		win.blit(self.img, (25, 300))

	def buy_draw(self,win): # Draws Buy BTN Image
		draw_x = 1060
		draw_y = self.y
		win.blit(self.img, (draw_x, draw_y))

	def update(self): #updates button position
		self.x = self.menu.x
		self.y = self.menu.y

class VerticalButton(Button):
	def __init__(self, x, y, img, name, cost):
		self.name = name
		self.img = img
		self.x = x
		self.y = y
		self.width = self.img.get_width()
		self.height = self.img.get_height()
		self.cost = cost

class Menu:
	def __init__(self, tower, x,y, img, item_cost):
		self.x = x
		self.y = y

		self.width = img.get_width()
		self.height = img.get_height()

		self.tower = tower

		# img + btn
		self.bg = img
		self.buttons = []
		self.items = 0
		self.item_cost = item_cost
		# fonts
		self.font = pygame.font.SysFont("Helvetica", 20)

	def add_btn(self, img, name): # Menu Add BTN
		self.items += 1
		self.buttons.append(Button(self, img, name))

	def get_item_cost(self): # gets cost of upgrade to next level
		return self.item_cost[self.tower.level - 1]

	def draw(self, win):
		win.blit(self.bg, (10, 160))
		for item in self.buttons:
			item.tower_draw(win)

			# Name of tower
			n = self.font.render("Name:", 1, WHITE)
			name = self.font.render(str(self.tower.name), 1, WHITE)
			win.blit(n, (25, 170))
			win.blit(name, (75, 170))

			# Attack DMG tower
			att = self.font.render("Attack DMG:", 1, WHITE)
			dmg = self.font.render(str(self.tower.damage), 1, WHITE)
			win.blit(att, (25 ,200))
			win.blit(dmg, (125, 200))

			# Attack Speed Tower
			s = self.font.render("Attack Speed:", 1, WHITE)
			speed = self.font.render(str(self.tower.att_speed), 1, WHITE)
			win.blit(s, (25, 230))
			win.blit(speed, (130, 230))

			# Cost of Tower
			money = self.font.render(str(self.item_cost[self.tower.level - 1]), 1, WHITE)
			win.blit(pokecash, (25, 255))
			win.blit(money, (80, 275))

	def get_clicked(self, X, Y): # Check if BTN is clicked
		for btn in self.buttons:
			if btn.click(X,Y):
				return btn.name
		return None

	def update(self):
		for btn in self.buttons:
			btn.update()

# Buy Menu
class VerticalMenu(Menu):
	def __init__(self, x, y, img):
		self.x = x
		self.y = y

		self.width = img.get_width()
		self.height = img.get_height()

		# img + btn
		self.bg = img
		self.buttons = []
		self.items = 0

		# fonts
		self.font = pygame.font.SysFont("Helvetica", 20)

	def add_btn(self, img, name, cost):#adds buttons to menu
		self.items += 1
		btn_x = 1060
		btn_y = (self.y - 175) + (self.items-1)*80 # seperate by 80 pixels
		self.buttons.append(VerticalButton(btn_x, btn_y, img, name, cost))

	def get_item_cost(self, name):
		for btn in self.buttons:
			if btn.name == name:
				return btn.cost
		return -1

	#drawing side menu
	def draw(self, win):
		menu_x = 1200 - self.bg.get_width()
		menu_y = self.bg.get_height()-200
		win.blit(self.bg, (menu_x, menu_y)) # location of menu

		for item in self.buttons:
			item.buy_draw(win)

			# Buy Price
			cost = self.font.render(str(item.cost), 1, (255, 255, 255))
			cost_x = 1155
			cost_y = item.y + 15
			win.blit(cost, (cost_x, cost_y))

			# Buy IMG
			win.blit(buy_pokecash, (cost_x - 30, cost_y))
