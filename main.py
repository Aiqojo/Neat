import Board
import pygame
import time
import constants
import Agent
import random

def main():

    pygame.init()

    board = Board.Board()
    board.create_window()
    board.get_empty_spawn_cells()
    board.randomize_lava()
    board.draw_grid()
    board.create_exit()
    board.build_bridge()

    arr = []
    
    for i in range(20):
        agent = Agent.Agent(board)
        board.add_agent(agent)
        arr.append((agent.x, agent.y))

    # Randomly move agent around
    for i in range(500):
        pygame.display.flip()
        time.sleep(.1)
        board.randomly_move_agents()        
        pygame.display.flip()
        #time.sleep(.1)

    board.run()
    

if __name__ == '__main__':
    main()

# logic for when agent moves onto cell
# make agents bump into each other
# give them a chance to push other agent and take its place
# if it's a lava cell, kill the agent