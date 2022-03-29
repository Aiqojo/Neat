import Board
import pygame
import time
import constants
import Agent
import random


def main():

    pygame.init()

    board = Board.Board()

    for i in range(20):
        agent = Agent.Agent(board)
        board.add_agent(agent)

    # Randomly move agent around
    while board.agent_list:
        pygame.display.flip()
        #time.sleep(.05)
        board.randomly_move_agents()
        pygame.display.flip()
        #time.sleep(.1)

    agents_left = 0
    for i in range(constants.WINDOW_WIDTH // constants.CELL_SIZE):
        for j in range(constants.WINDOW_HEIGHT // constants.CELL_SIZE):
            if board.cells[i][j].agent:
                agents_left += len(board.cells[i][j].agent)

    print("AGENTS LEFT: " + str(agents_left))

    board.run()


if __name__ == '__main__':
    main()
