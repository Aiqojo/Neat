import pygame

class Board:

    def init(self, width, height, cell_size):

        self.screen = self.create_window()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cell_count = width * height
        self.cells = [False] * self.cell_count
        self.neighbour_count = [0] * self.cell_count
        self.GREY = (105, 105, 105)
        self.WHITE = (255, 255, 255)
        self.WINDOW_HEIGHT = 800
        self.WINDOW_WIDTH = 800


    # This method creates a pygame window with a white background
    def create_window(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 800))
        screen.fill(self.GREY)
        return screen

    def draw_grid(self, screen):
        blockSize = 40 #Set the size of the grid block
        for x in range(0, self.WINDOW_WIDTH, blockSize):
            for y in range(0, self.WINDOW_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(screen, self.WHITE, rect, 1)

    def initialize(self):
        self.draw_grid(self.screen)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.update()