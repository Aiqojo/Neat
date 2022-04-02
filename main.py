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
board = Board.Board()


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
    board.reset_board()
    for i in genomes:
        agent = Agent.Agent(board, i)
        board.add_agent(agent)

    # Set up genomes and networks
    for genomeid, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)

    # Reset agent positions
    #board.reset_agents()

    # #Randomly move agent around
    # while board.alive_agents > 0:
    #     pygame.display.flip()
    #     time.sleep(.05)
    #     board.randomly_move_agents()
    #     pygame.display.flip()
    #     #time.sleep(.1)

    # Run the game
    max_frames = 100
    pygame.display.flip()
    time.sleep(.2)

    while board.alive_agents > 0 and max_frames > 0:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # For each agent, get the output from the network and move it
        agent_index = 0
        for agent in ge:
            agent = board.agent_list[agent_index]
            # If the agent is in a cell it has been in previously, subtract fitness equal to the amount of time it has been in that cell
            #ge[agent_index].fitness -= agent.get_cell_history(board.cells[agent.x // constants.CELL_SIZE][agent.y // constants.CELL_SIZE])
            # Add 5 to fitness to give the agent a little incentive for staying alive
            ge[agent_index].fitness += 1
            # Get adjacent cells
            adj = agent.get_adjacent_terrain()
            # Get the output from the network
            output = nets[board.agent_list.index(agent)].activate((float(adj[0]), float(adj[1]), float(adj[2]), float(adj[3]), float(adj[4]), float(adj[5]), float(adj[6]),
                                                                   float(adj[7]), float(agent.x), float(agent.y), float(board.exit_x), float(board.exit_y)))

            # Move the agent
            direction = output.index(max(output))
            if direction == 0:
                agent.move(-1, -1)
            elif direction == 1:
                agent.move(0, -1)
            elif direction == 2:
                agent.move(1, -1)
            elif direction == 3:
                agent.move(-1, 0)
            elif direction == 4:
                agent.move(1, 0)
            elif direction == 5:
                agent.move(-1, 1)
            elif direction == 6:
                agent.move(0, 1)
            elif direction == 7:
                agent.move(1, 1)

            # Check if agent is dead
            if not agent.alive:
                ge[agent_index].fitness -= 100
                board.alive_agents -= 1
                board.agent_list.remove(agent)
                nets.pop(agent_index)
                ge.pop(agent_index)
            else:
                if agent.reached_exit():
                    ge[agent_index].fitness += 2500
                    board.alive_agents -= 1
                    board.agent_list.remove(agent)
                    nets.pop(agent_index)
                    ge.pop(agent_index)
                agent_index += 1

        # Update the board
        pygame.display.flip()
        #time.sleep(.001)
        max_frames -= 1
        #print("AGENTS ALIVE: " + str(board.alive_agents))

    # Add distance fitness to each genome
    agent_index = 0
    for agent in ge:
        agent = board.agent_list[agent_index]
        distance = max(abs(agent.x - board.exit_x),
                       abs(agent.y - board.exit_y))
        ge[agent_index].fitness += 1000*(1 / distance)
        agent_index += 1

    #Save the winner
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

    winner = p.run(main, 500)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.ini')
    run(config_path)
