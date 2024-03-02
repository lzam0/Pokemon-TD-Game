from game import Game
import pygame
import os

from settings import *

class MainMenu:
    def __init__(self, win):
        self.width = WIDTH
        self.height = HEIGHT

    def run(self):
        run = True

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONUP:
                    # check if hit start btn
                    x, y = pygame.mouse.get_pos()