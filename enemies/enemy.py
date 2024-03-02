import pygame
import math


class Enemy:
    imgs = []
    def __init__(self):
        # sprite size
        self.width = 64
        self.height = 64

        # sprite info
        self.health = 1
        self.max_health = 0
        
        # animation
        self.animation_count = 1
        self.anim_last_update = pygame.time.get_ticks()
        self.anim_speed = 200
        self.vel = 1.2

        # path | list of points on the map
        self.path = [(95, 310),(545, 310), (545, 475), (355, 475), (355, 200), (540, 200), (675, 200),(675, 475),(975, 475), (975, 310),(975, -35)]
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.path_pos = 0
        self.dis = 0
        
        self.img = [] 
        self.flipped = False

    def draw(self, win, dt): # Draw Enemy with given images

        self.img = self.imgs[self.animation_count]
        now = pygame.time.get_ticks()
        if now - self.anim_last_update > self.anim_speed:
            self.anim_last_update = now
            self.animation_count += 1
            if self.animation_count >= len(self.imgs):
                self.animation_count = 0

        # shows path positions on the screen
        """
        for dot in self.path:
            pygame.draw.circle(win, (255,0,0), dot, 10, 0)
        """
        win.blit(self.img, (self.x - self.img.get_width()/2 , self.y - self.img.get_height()/2))
        self.move(dt)
        self.draw_health(win)

    def draw_health(self, win): # Draw health above enemy
        #healthbar
        length = 50
        move_by = length / self.max_health
        health_bar = move_by * self.health

        pygame.draw.rect(win, (0, 0, 0), (self.x-30, self.y - 35, health_bar, 10), 2) # outline
        #pygame.draw.rect(win, (255,0,0), (self.x-30, self.y-75, length, 10), 0) # length
        pygame.draw.rect(win, (0, 255, 0), (self.x-30, self.y - 35, health_bar, 10), 0) # hp left

    def collide(self, x, y): # Returns if position has hit enemy

        if x < self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False

    def move(self, dt):  # moving algorithm for enemy with delta time (dt)
        if self.path_pos >= len(self.path):
            # Enemy has reached the end of the path, stop moving
            return False

        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len(self.path):
            x2, y2 = (975, -25)
        else:
            x2, y2 = self.path[self.path_pos + 1]

        dirn = ((x2 - x1) * 2, (y2 - y1) * 2)
        length = math.sqrt(dirn[0] ** 2 + dirn[1] ** 2)
        dirn = (dirn[0] / length, dirn[1] / length)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # Check if the enemy has reached the next point
        if dirn[0] >= 0:  # moving right
            if dirn[1] >= 0:  # moving down
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1  # move to the next path position
            else:  # moving up
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1
        else:  # moving left
            if dirn[1] >= 0:  # moving down
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:  # moving up
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1

        # Ensure path_pos is within valid range
        if self.path_pos >= len(self.path):
            self.path_pos = len(self.path) - 1

        return True

    def hit(self): # Removes health regarding dmg taken
        self.health -= 1
        if self.health <= 0:
            return True
        return False
