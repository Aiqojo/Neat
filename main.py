import Board
import pygame
import time
import constants
import Agent
import random

def main():
    pygame.init()


    board = Board.Board()
    board.init()
    board.randomize_lava()
    board.draw_grid()
    board.create_exit()
    board.build_bridge()
    agent_test = Agent.Agent()

    # Randomly move agent around
    for i in range(500):
        agent_test.find_path(board)
        agent_test.draw(board)
        board.draw_grid()
        pygame.display.flip()
        agent_test.reached_exit(board)
        print(agent_test.x, agent_test.y)
        time.sleep(.1)



    board.run()
    

if __name__ == '__main__':
    main()

