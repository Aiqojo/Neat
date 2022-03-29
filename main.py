import Board
import pygame
import time
import constants
import Agent
import random

def main():

    pygame.init()

    board = Board.Board()
    board.randomize_lava()
    board.draw_grid()
    board.create_exit()
    board.build_bridge()

    print(board.empty_spawn_cells)
    
    for i in range(25):
        agent = Agent.Agent(board)
        board.add_agent(agent)
    
    # Randomly move agent around
    for i in range(500):
        board.randomly_move_agents()        
        pygame.display.flip()
        time.sleep(.1)

    board.run()
    

if __name__ == '__main__':
    main()

# oh god i made a bunch of init instaed of actualy constructors look that shit up
# logic for when agent moves onto cell
# make agents bump into each other
# give them a chance to push other agent and take its place
# if it's a lava cell, kill the agent