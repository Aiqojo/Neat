import pygame
import constants
import random

class Cell:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.terrain = "rock"


    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))
