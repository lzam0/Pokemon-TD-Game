import pygame, os, math, time

from menu.menu import Menu

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assests", "menu.png")), (175, 250))

class Tower:
    """
    Abstract class for towers
    """
    tower_imgs = []
    def __init__(self,x,y):
        self.name = ""
        
        # positioning | on map
        self.x = x
        self.y = y

        # sprite size
        self.width = self.height = 64
        
        # prices
        self.sell_price = [0,0,0]
        self.price = [0,0,0]

        # level
        self.level = 1

        # menu 
        self.selected = False
        # sprite images
        self.tower_img = []
        self.tower_count = 1
        self.tower_anim_last_update = pygame.time.get_ticks()
        self.tower_anim_speed = 200

        # attack
        self.damage = 5
        self.range = 0
        self.hit_timer = time.time()
        self.att_speed = 1
        self.inRange = False

        # placement
        self.place_color = (0,0,255, 100)


    def draw(self, win): #Draws Tower with given images

        self.tower_img = self.tower_imgs[self.tower_count]
        now = pygame.time.get_ticks()
        if now - self.tower_anim_last_update > self.tower_anim_speed:
            self.tower_anim_last_update = now
            self.tower_count += 1
            if self.tower_count >= len(self.tower_imgs):
                self.tower_count = 0

        """
        img = self.tower_imgs[self.level - 1]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))
        """
        # Draw Tower only when enemy in range
        win.blit(self.tower_img, (self.x - self.tower_img.get_width()/2 , self.y - self.tower_img.get_height()/2))

        if self.selected:
            self.menu.draw(win)
        
        self.draw_radius(win)

    def draw_radius(self,win): # draw range circle
        if self.selected == True:
            surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)
            
            win.blit(surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self, win):  # draw range circle
        surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (32,32), 32, 0)
        win.blit(surface, (self.x - 32, self.y - 32))

    def click(self, X, Y): # Returns if tower has been clicked on
        if self.level <= len(self.tower_imgs):
            img = self.tower_imgs[self.level - 1]
        else:
            img = self.tower_imgs[-1]  # Use the last tower image if level exceeds available images

        if X <= self.x - img.get_width() // 2 + self.width and X >= self.x - img.get_width() // 2:
            if Y <= self.y + self.height - img.get_height() // 2 and Y >= self.y - img.get_height() // 2:
                return True
        return False

    def sell(self): #selling tower for x price
        return self.sell_price[self.level-1]

    def upgrade(self): # ugrade tower for given cost
        if self.level + 1 < len(self.tower_imgs):
            self.level += 1
            self.damage += self.damage * 2

    def get_upgrade_cost(self): # return the upgrade cost, if 0 then can't upgrade anymore
        # Check if the tower can be upgraded further
        if self.level < len(self.price):
            return self.price[self.level - 1]  # Return the upgrade cost for the current level
        else:
            return 0  # Return 0 if the tower is already at max level

    def move(self, x, y): # moving enemy tower
        self.x = x
        self.y = y

    
    def change_range(self,r):
        self.range = r

    def attack(self, enemies): # Attack First Enemy in range

        money = 0
        self.inRange = False
        enemy_list = [] # enemies within range of tower
        

        for enemy in enemies:
            x = enemy.x
            y = enemy.y

            dis = math.sqrt((self.x - enemy.img.get_width()/2 - x)**2 + (self.y - enemy.img.get_height()/2 - y)**2)

            # if enemy in range then add to enemy_closet list
            if dis < self.range:
                self.inRange = True
                enemy_list.append(enemy)

            if len(enemy_list) > 0:
                first_enemy = enemy_list[0] # get first enemy
                if time.time() - self.hit_timer >= self.att_speed: # timer for enemy
                    self.hit_timer = time.time()
                    enemy.health = enemy.health - self.damage # take away enemy health
                    if first_enemy.hit() == True:
                        money = first_enemy.money * 2
                        enemies.remove(first_enemy) # remove enemy off screen when hp <= 0
        return money

    def collide(self, otherTower):
            x2 = otherTower.x
            y2 = otherTower.y

            dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
            if dis >= 100:
                return False
            else:
                return True