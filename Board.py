import pygame
import random
import sys
import Cell
import constants
import numpy as np
import time


class Board:

    agent_list = []

    def __init__(self):

        # Create 2d array
        self.cells = np.empty((constants.WINDOW_WIDTH // constants.CELL_SIZE,
                               constants.WINDOW_HEIGHT // constants.CELL_SIZE), dtype=Cell.Cell)

        # Create pygame window
        self.screen = pygame.display.set_mode(
            (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.create_window()

        self.cell_count = constants.WINDOW_WIDTH // constants.CELL_SIZE * \
            constants.WINDOW_HEIGHT // constants.CELL_SIZE

        self.create_window()
        self.get_empty_spawn_cells()
        self.randomize_lava()
        self.draw_grid()
        self.create_exit()
        self.build_bridge()

    # To run the game

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        sys.exit()
            pygame.display.flip()

    # This method creates a pygame window with a grey background
    def create_window(self):
        pygame.init()
        pygame.display.set_caption("NeatDungeon")

        # This loop creates a cell object and adds it to the board
        for i in range(0, constants.WINDOW_WIDTH // constants.CELL_SIZE):
            for j in range(0, constants.WINDOW_HEIGHT // constants.CELL_SIZE):
                self.cells[i][j] = Cell.Cell(i * constants.CELL_SIZE, j * constants.CELL_SIZE,
                                             constants.CELL_SIZE)
                self.cells[i][j].draw(self.screen, constants.GROUND_COLOR)
        self.draw_grid()

    # This method draws the grid over top of the cells
    def draw_grid(self):
        for x in range(0, constants.WINDOW_WIDTH, constants.CELL_SIZE):
            pygame.draw.line(self.screen, constants.BLACK,
                             (x, 0), (x, constants.WINDOW_HEIGHT))
        for y in range(0, constants.WINDOW_HEIGHT, constants.CELL_SIZE):
            pygame.draw.line(self.screen, constants.BLACK,
                             (0, y), (constants.WINDOW_WIDTH, y))

    def get_empty_spawn_cells(self):
        arr = []
        for x in range(0, constants.SAFE_ZONE_WIDTH // constants.CELL_SIZE):
            for y in range(0, constants.WINDOW_HEIGHT // constants.CELL_SIZE):
                if len(self.cells[x][y].agent) == 0:
                    arr.append(self.cells[x][y])
        self.empty_spawn_cells = arr

    # Randomly places lava cells
    def randomize_lava(self):
        for i in range(constants.SAFE_ZONE_WIDTH // constants.CELL_SIZE,
                       (constants.WINDOW_WIDTH - constants.SAFE_ZONE_WIDTH) // constants.CELL_SIZE):
            for j in range(0, constants.WINDOW_HEIGHT // constants.CELL_SIZE):
                if random.randint(0, 100) < constants.LAVA_CHANCE:
                    self.cells[i][j].terrain = "lava"
                    self.cells[i][j].color = constants.LAVA_COLOR
                    self.cells[i][j].draw(self.screen, constants.LAVA_COLOR)
                    self.draw_grid()

        self.draw_grid()

    # Creates one exit within the right most safe zone
    def create_exit(self):
        exit_cell_x = random.randint(((constants.WINDOW_WIDTH - constants.SAFE_ZONE_WIDTH)
                                      // constants.CELL_SIZE),
                                     (constants.WINDOW_WIDTH // constants.CELL_SIZE) - 1)
        exit_cell_y = random.randint(
            0, constants.WINDOW_HEIGHT // constants.CELL_SIZE - 1)
        self.cells[exit_cell_x][exit_cell_y].terrain = "exit"
        self.cells[exit_cell_x][exit_cell_y].draw(
            self.screen, constants.EXIT_COLOR)
        self.draw_grid()

    # Creates a bridge between the left most safe zone and the right most safe zone
    def build_bridge(self):
        bridge_y = random.randint(
            0, constants.WINDOW_HEIGHT / constants.CELL_SIZE)

        for i in range(max(0, bridge_y - constants.BRIDGE_WIDTH // 2),
                       min(constants.WINDOW_HEIGHT // constants.CELL_SIZE,
                           bridge_y + constants.BRIDGE_WIDTH // 2)):
            for j in range(constants.SAFE_ZONE_WIDTH // constants.CELL_SIZE,
                           ((constants.WINDOW_WIDTH - constants.SAFE_ZONE_WIDTH) // constants.CELL_SIZE)):
                self.cells[j][i].terrain = "wood"
                self.cells[j][i].color = constants.WOOD_COLOR
                self.cells[j][i].draw(self.screen, constants.WOOD_COLOR)
            self.draw_grid()

        self.draw_grid()

    def add_agent(self, agent):
        self.agent_list.append(agent)

        cell = random.choice(self.empty_spawn_cells)

        agent.x = cell.x
        agent.y = cell.y
        cell.agent.append(agent)
        self.empty_spawn_cells.remove(cell)
        agent.draw(self)

    # This method randomly moves all the agents

    def randomly_move_agents(self):
        for agent in self.agent_list:
            if agent.alive:
                agent.random_move()
                agent.draw(self)
                # time.sleep(.25)
        self.draw_grid()
