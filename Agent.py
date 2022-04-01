import pygame
import constants
import random
import time


class Agent:

    def __init__(self, board, id):

        self.board = board
        self.id = id

        #pygame.sprite.Sprite.__init__(self)
        self.initialize_agent_image()

        self.x = 0
        self.y = 0
        self.previous_x = 0
        self.previous_y = 0
        self.alive = True
        self.score = 0

        # STATISTICS
        self.health = 100
        self.strength = random.randint(1, 20)

    def initialize_agent_image(self):
        pygame.sprite.Sprite.__init__(self)
        # Specific agent image
        self.agent_specific_image = pygame.Surface(
            (constants.CELL_SIZE - 5, constants.CELL_SIZE - 5))
        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        self.agent_specific_image.fill(self.color)

        # Universal agent image
        self.universal_agent = pygame.Surface(
            (constants.CELL_SIZE, constants.CELL_SIZE))
        self.universal_agent_color = constants.AGENT_COLOR
        self.universal_agent.fill(self.universal_agent_color)

    # Draws a cell to fill the agent's previous position and draws the agent's current position
    def draw(self, board):
        if self.alive:
            # Drawing the previous cell
            curr_cell = board.cells[self.previous_x //
                                    constants.CELL_SIZE][self.previous_y // constants.CELL_SIZE]
            curr_cell.draw(board.screen)

            # Creates a border square to help show that this cell is occupied by an agent
            board.screen.blit(self.universal_agent, (self.x, self.y))
            # Then draws individual agent's color
            board.screen.blit(self.agent_specific_image,
                              (self.x + 3, self.y + 3))

    # Moves the agent in the given direction and keeps in bounds
    def move(self, x, y):
        #print("AGENT X AND Y: ", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
        #print("MOVE:", x // constants.CELL_SIZE, y // constants.CELL_SIZE)
        #print("CELL X AND Y:", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
        #print("AGENT:", self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent)

        if self.alive:
            self.board.cells[self.x // constants.CELL_SIZE][self.y //
                                                            constants.CELL_SIZE].agent.remove(self)

            # Changing coordinates
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

            # Adds agent to next cell
            self.board.cells[self.x // constants.CELL_SIZE][self.y //
                                                            constants.CELL_SIZE].agent.append(self)

            # Checks if move is valid
            other_cell = self.board.cells[self.x //
                                          constants.CELL_SIZE][self.y // constants.CELL_SIZE]

            # Collision checks
            self.check_collision(other_cell)
            # Have to re-enter self.x and self.y because the agent could've been moved to another cell, and not into other_cell
            self.terrain_check(self.board.cells[self.x //
                                          constants.CELL_SIZE][self.y // constants.CELL_SIZE])

            # Draws the agent
            self.draw(self.board)
            self.board.draw_grid()

    # Method checks if the agent is in the same cell as another agent

    def check_collision(self, cell):
        if cell.agent:
            for other_agent in cell.agent:
                if other_agent != self:
                    # If collision remove agent at its current cell
                    if self.health > 0:
                        self.board.cells[self.x // constants.CELL_SIZE][self.y //
                                                                        constants.CELL_SIZE].agent.remove(self)
                    # Move it back to its previous cell
                    self.x = self.previous_x
                    self.y = self.previous_y
                    # Add it back to the previous cell
                    self.board.cells[self.x // constants.CELL_SIZE][self.y //
                                                                    constants.CELL_SIZE].agent.append(self)

    # Checks the current terrain and changes the agent's health accordingly the calls check_collision
    def terrain_check(self, cell):
        if cell.get_terrain() == "lava":
            self.change_health(-25)
            #score -= 50
            #print("DAMAGE TAKEN AT:", self.x // constants.CELL_SIZE, self.y // constants.CELL_SIZE)
            #print("HEALTH: ", self.health)
            if self.health <= 0:
                self.die()
                #print("DEAD AT:" + str(self.x // constants.CELL_SIZE) + "," + str(self.y // constants.CELL_SIZE))
        # Checks if the agent is in the same cell as another agent

    # Kills the agent
    def die(self):
        # Gets cell
        curr_cell = self.board.cells[self.x //
                                     constants.CELL_SIZE][self.y // constants.CELL_SIZE]
        # Draws red square to show that the agent is dead
        # curr_cell.draw(self.board.screen, constants.RED)
        curr_cell.draw(self.board.screen)
        # Removes the agent from the cell
        curr_cell.agent.remove(self)

        # Removes the agent from the board
        prev_cell = self.board.cells[self.previous_x //
                                     constants.CELL_SIZE][self.previous_y // constants.CELL_SIZE]
        prev_cell.draw(self.board.screen)

        self.alive = False
        self.score = -1000

        # Removes from board list
        self.board.alive_agents -= 1

    def is_alive(self):
        return self.alive

    # This method returns a list of all of the adajcent cells terrain
    def get_adjacent_terrain(self):
        # Rock is 0, lava is 1, wood is 2, not exist/wall = 3
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0),
               (1, 1), (1, -1), (-1, 1), (-1, -1)]
        adjacent_terrain = []
        for x, y in dir:
            try:
                adjacent_terrain.append(self.board.cells[(self.x //
                                                          constants.CELL_SIZE) + x][(self.y // constants.CELL_SIZE) + y].get_terrain())
            except:
                adjacent_terrain.append("wall")

        adj_arr = []
        for cell in adjacent_terrain:
            if cell == "rock":
                adj_arr.append(0)
            elif cell == "lava":
                adj_arr.append(1)
            elif cell == "wood":
                adj_arr.append(2)
            else:
                adj_arr.append(3)

        return adj_arr

    # Checks if the agent has reached the exit
    def reached_exit(self, board):
        if "exit" in board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].get_terrain():
            self.die(board)
            self.change_score(100)
            return True

    def set_stats(self):
        self.health = 100
        self.strength = random.randint(1, 20)

    def change_health(self, health):
        self.health += health
        if (self.health / 100) < 1:
            for i in self.color:
                i *= (self.health / 100)

    def random_move(self):
        self.move(random.randint(-1, 1), random.randint(-1, 1))
