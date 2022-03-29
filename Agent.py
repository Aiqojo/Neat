from ast import Constant
from tkinter.tix import CELL
import pygame
import constants
import random
import time

class Agent:

    def __init__(self, board):
        
        self.board = board

        #pygame.sprite.Sprite.__init__(self)
        self.initialize_agent_image()

        self.x = 0
        self.y = 0
        self.previous_x = 0
        self.previous_y = 0
        self.alive = True
        self.score = 0

        self.set_stats()

    def initialize_agent_image(self):
        pygame.sprite.Sprite.__init__(self)
        # Specific agent image
        self.agent_specific_image = pygame.Surface((constants.CELL_SIZE - 5, constants.CELL_SIZE - 5))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.agent_specific_image.fill(self.color)

        # Universal agent image
        self.universal_agent = pygame.Surface((constants.CELL_SIZE, constants.CELL_SIZE))
        self.universal_agent_color = constants.AGENT_COLOR
        self.universal_agent.fill(self.universal_agent_color)

    # Draws a cell to fill the agent's previous position and draws the agent's current position
    def draw(self, board):
        if self.alive:
            curr_cell = board.cells[self.previous_x // constants.CELL_SIZE][self.previous_y // constants.CELL_SIZE]
            curr_cell.draw(board.screen, curr_cell.color)
            # Creates a border square to help show that this cell is occupied by an agent
            board.screen.blit(self.universal_agent, (self.x, self.y))
            # Then draws individual agent's color
            board.screen.blit(self.agent_specific_image, (self.x + 3, self.y + 3))
        
        

    # Moves the agent in the given direction and keeps in bounds
    def move(self, x, y):
        print("MOVE AT:", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE, self)
        self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent.remove(self)
        
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
        
        self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent.append(self)
        print("MOVE TO:", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)

        # Checks if move is valid
        other_cell = self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE]

        # Collision checks
        self.check_collision(other_cell)
        self.terrain_check(other_cell)
        
    # Method checks if the agent is in the same cell as another agent
    def check_collision(self, cell):
        if cell.agent:
            for other_agent in cell.agent:
                if other_agent != self:
                    print("COLLISION AT: ", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
                    # If collision remove agent at its current cell
                    if self.health > 0:
                        self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent.remove(self)
                    # Move it back to its previous cell
                    self.x = self.previous_x
                    self.y = self.previous_y
                    # Add it back to the previous cell
                    self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent.append(self)

    # Checks the current terrain and changes the agent's health accordingly the calls check_collision
    def terrain_check(self, cell):
        if cell.get_terrain() == "lava":
            self.change_health(-20)
            print("DAMAGE TAKEN AT:", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
            print("HEALTH: ", self.health)
            if self.health <= 0:
                self.die()
                print("DEAD AT:" + str(self.x // constants.CELL_SIZE) + "," + str(self.y // constants.CELL_SIZE))
        # Checks if the agent is in the same cell as another agent
        
            
    # Checks if the agent has reached the exit
    def reached_exit(self, board):
        if "exit" in board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].get_terrain():
            self.die(board)
            self.change_score(100)
            return True

    # Kills the agent
    def die(self):
        # self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].draw(self.board.screen, self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].color)
        cell = self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE]
        cell.draw(self.board.screen, constants.RED)
        cell.agent.remove(self)
        cell.draw(self.board.screen, cell.color)
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

    def set_stats(self):
        self.health = 100
        self.strength = random.randint(1, 20)

    def get_strength(self):
        return self.strength

    def get_health(self):
        return self.health

    def change_health(self, health):
        self.health += health
        if (self.health / 100) < 1:
            for i in self.color:
                i *= (self.health / 100)
    
    def change_strength(self, strength):
        self.strength += strength
    
    def get_stats(self):
        return self.health, self.strength

    # # Method checks the strength of the agent compared to the strength of the other agent in the cell and if the agent is stronger, pushes the other agent
    # def push_agent(self, other_agent):
    #     strength = self.get_strength()
    #     other_strength = other_agent.get_strength()
    #     # If the agent is stronger, pushes the other agent one cell in the direction it is moving
    #     if strength > other_strength:
    #         other_agent.move((self.x - self.previous_x) // constants.CELL_SIZE, (self.y - self.previous_y) // constants.CELL_SIZE)
    #         self.draw(self.board)
    #         other_agent.draw(self.board)
    #     else:
            
    #         # Remove the agent from the cell it is currently in
    #         self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent.remove(self)
    #         # Add the agent to the previous cell
    #         self.board.cells[self.previous_x // constants.CELL_SIZE][self.previous_y // constants.CELL_SIZE].agent.append(self)

    #         self.x = self.previous_x
    #         self.y = self.previous_y