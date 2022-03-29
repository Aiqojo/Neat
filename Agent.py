import pygame
import constants
import random
import time

class Agent:

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)
        
        self.x = random.randint(0, constants.SAFE_ZONE_WIDTH // constants.CELL_SIZE) * constants.CELL_SIZE - constants.CELL_SIZE * 2
        self.y = random.randint(0, constants.WINDOW_HEIGHT // constants.CELL_SIZE)  * constants.CELL_SIZE - constants.CELL_SIZE
        self.previous_x = 0
        self.previous_y = 0
        
        self.score = 0
        self.alive = True
        
        self.image = pygame.Surface((constants.CELL_SIZE, constants.CELL_SIZE))
        self.image.fill(constants.AGENT_COLOR)

    # Draws a cell to fill the agent's previous position and draws the agent's current position
    def draw(self, board):
        curr_cell = board.cells[self.previous_x // constants.CELL_SIZE][self.previous_y // constants.CELL_SIZE]
        curr_cell.draw(board.screen, curr_cell.color)
        board.screen.blit(self.image, (self.x, self.y))

    # Moves the agent in the given direction and keeps in bounds
    def move(self, x, y):
        self.previous_x = self.x
        self.previous_y = self.y

        x *= constants.CELL_SIZE
        y *= constants.CELL_SIZE

        # Moves the agents x position but keeps it in bounds
        if self.x + x < 0:
            self.x = 0
        elif self.x + x > constants.WINDOW_WIDTH - constants.CELL_SIZE:
            self.x = constants.WINDOW_WIDTH - constants.CELL_SIZE
        else:
            self.x += x
        
        # Moves the agents y position but keeps it in bounds
        if self.y + y < 0:
            self.y = 0
        elif self.y + y > constants.WINDOW_HEIGHT - constants.CELL_SIZE:
            self.y = constants.WINDOW_HEIGHT - constants.CELL_SIZE
        else:
            self.y += y

    # Checks if the agent has reached the exit
    def reached_exit(self, board):
        if "exit" in board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].get_terrain():
            self.die(board)
            self.change_score(100)
            return True

    # Kills the agent
    def die(self, board):
        board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].draw(board.screen, constants.GROUND_COLOR)
        self.alive = False
        self.score = -100

    def change_score(self, score):
        self.score += score

    def is_alive(self):
        return self.alive

    def get_score(self):
        return self.score

    def get_position(self):
        return (self.x, self.y)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    