import Board
import pygame
import time
import constants
import Agent
import random
import os
import neat
import pickle
import math

# EXIT DISSPAEARES WHEN REACHED FIX
# ALSO END WHEN 1 REACHES EXIT
# ALSO MAKE THE GET TERRAIN FUNCTION RETURN 4 FOR IF THERE IS AN AGENT IN THAT SQUARE
# MAKE PREVIOUS CELL BE ITS ACTUAL PROPER COLOR

def main(genomes, config):
    pygame.init()

    # board = Board.Board()
    # for i in range(20):
    #     agent = Agent.Agent(board, i)
    #     board.add_agent(agent)

    # # Randomly move agent around
    # while board.alive_agents > 0:
    #     pygame.display.flip()
    #     #time.sleep(.05)
    #     board.randomly_move_agents()
    #     pygame.display.flip()
    #     time.sleep(.1)

    nets = []
    ge = []

    # Create the board and agents
    board = Board.Board()
    for i in genomes:
        agent = Agent.Agent(board, i)
        board.add_agent(agent)

    # Set up genomes and networks
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)

    # Reset agent positions
    #board.reset_agents()

    # Run the game
    max_frames = 100
    pygame.display.flip()
    while board.alive_agents > 0 and max_frames > 0:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit
                break

        for x, agent in enumerate(board.agent_list):
            if not agent.alive:
                    ge[x].fitness -= 50
                    nets.pop(board.agent_list.index(agent))
                    ge.pop(board.agent_list.index(agent))
                    board.agent_list.pop(board.agent_list.index(agent))
                    

        for x, agent in enumerate(ge):
            #print("GE LENGTHL", len(ge))
            agent = board.agent_list[x]
            if agent.alive:
                # If the agent is in the same cell, it loses one fitness
                if agent.previous_x == agent.x and agent.previous_y == agent.y:
                    ge[x].fitness -= 5

                ge[x].fitness += 1

                adj = agent.get_adjacent_terrain()
                # The input is the
                output = nets[board.agent_list.index(agent)].activate((float(adj[0]), float(adj[1]), float(adj[2]), float(adj[3]), float(adj[4]), float(adj[5]), float(adj[6]),
                                                                       float(adj[7]), float(agent.x), float(agent.y), float(board.exit_x), float(board.exit_y)))
                
                direction = output.index(max(output))
                
                if direction == 0:
                    agent.move(-1,-1)
                elif direction == 1:
                    agent.move(0,-1)
                elif direction == 2:
                    agent.move(1,-1)
                elif direction == 3:
                    agent.move(-1,0)
                elif direction == 4:
                    agent.move(1,0)
                elif direction == 5:
                    agent.move(-1,1)
                elif direction == 6:
                    agent.move(0,1)
                elif direction == 7:
                    agent.move(1,1)

        pygame.display.flip()
        time.sleep(.05)

        max_frames -= 1

    for x, agent in enumerate(ge):
        agent = board.agent_list[x]
        if agent.alive:
            ge[x].fitness += 5
            # Finds distance of agent to exit
        dist = abs(agent.x - board.exit_x) + abs(agent.y - board.exit_y)
        if dist == 0:
            ge[x].fitness += 1000
        else:
            ge[x].fitness += 25*(.25/dist)
            
    # Save the winner
    with open('winner.pkl', 'wb') as output:
        pickle.dump(ge[0], output, 1)

    #board.run()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.ini')
    run(config_path)
