import Board
import pygame
import time
import constants

def main():
    pygame.init()


    board = Board.Board()
    board.init()
    board.randomize_lava()
    board.draw_grid()
    board.create_exit()
    board.build_bridge()
    
    




    board.run()
    

if __name__ == '__main__':
    main()

