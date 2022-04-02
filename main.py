import Board
import pygame
import constants
import Agent
import os
import neat
import pickle
import math

# EXIT DISSPAEARES WHEN REACHED FIX
# ALSO END WHEN 1 REACHES EXIT
# ALSO MAKE THE GET TERRAIN FUNCTION RETURN 4 FOR IF THERE IS AN AGENT IN THAT SQUARE
# MAKE PREVIOUS CELL BE ITS ACTUAL PROPER COLOR
global lava_num
lava_num = 0
global lava_chance
lava_chance = constants.LAVA_CHANCE
board = Board.Board(lava_chance)


def main(genomes, config):
    global lava_num
    lava_num += 1
    global lava_chance
    lava_chance = (15/(1+math.exp(-.0012*(lava_num-6000))))/2
    print("LAVA CHANCE", lava_chance)
    board.lava_chance = lava_chance
    pygame.init()

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

    # Run the game
    max_frames = 200
    #pygame.display.flip()
    #time.sleep(.1)

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

            ge[agent_index].fitness += 1
            # Get adjacent cells
            adj = agent.get_adjacent_terrain()
            # Get the output from the network

            displacement_x = board.exit_x - agent.x
            displacement_y = board.exit_y - agent.y

            output = nets[board.agent_list.index(agent)].activate((float(adj[0]), float(adj[1]), float(adj[2]),
                                                                   float(adj[3]), float(
                                                                       displacement_x),
                                                                   float(displacement_y)))

            # Move the agent
            direction = output.index(max(output))
            if direction == 0:
                agent.move(-1, 0)
            elif direction == 1:
                agent.move(1, 0)
            elif direction == 2:
                agent.move(0, -1)
            elif direction == 3:
                agent.move(0, 1)

            # Check if agent is dead
            if not agent.alive:
                # Fitness stuff
                ge[agent_index].fitness -= 250
                distance = (abs(agent.x - board.exit_x)) + \
                    abs(agent.y - board.exit_y)
                # Use .75 as exponent to make fitness gain from distance weaker here because the agent died
                ge[agent_index].fitness += 750*(1 / distance**.75)
                board.alive_agents -= 1
                board.agent_list.remove(agent)
                nets.pop(agent_index)
                ge.pop(agent_index)
                agent_index -= 1
            elif agent.reached_exit():
                ge[agent_index].fitness += 1000
                board.alive_agents -= 1
                board.agent_list.remove(agent)
                nets.pop(agent_index)
                ge.pop(agent_index)
                agent_index -= 1
            else:
                agent_index += 1

        # Update the board
        pygame.display.flip()
        #time.sleep(.005)
        max_frames -= 1
        #print("AGENTS ALIVE: " + str(board.alive_agents))

    # Add distance fitness to each genome
    agent_index = 0
    for agent in ge:
        agent = board.agent_list[agent_index]
        if agent.x <= constants.SAFE_ZONE_WIDTH:
            ge[agent_index].fitness += -500
        else:
            distance = (abs(agent.x - board.exit_x)) + \
                abs(agent.y - board.exit_y)
            ge[agent_index].fitness += 750*(1 / distance**.5)
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
    winner = p.run(main, 100000)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.ini')
    run(config_path)
