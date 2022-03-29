import pygame
import constants
import random

class Cell:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.terrain = "rock"
        self.color = constants.GROUND_COLOR

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))

    def get_terrain(self):
        return self.terrain

    def set_terrain(self, terrain):
        self.terrain = terrain

    def get_color(self):
        return self.color
    
    def set_color(self, color):
        self.color = color