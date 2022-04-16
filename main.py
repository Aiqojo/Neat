import Board
import pygame
import constants
import Agent
import os
import neat
import pickle
import math


global gen_num
# If restarting from checkpoint, put generation number here
gen_num = 0
global lava_chance
lava_chance = constants.LAVA_CHANCE
board = Board.Board(lava_chance)
max_frames = 1.5 * (constants.WINDOW_WIDTH // constants.CELL_SIZE *
                    constants.WINDOW_HEIGHT // constants.CELL_SIZE)


def main(genomes, config):
    # Having lava chance slowly increase via 2 s-curves
    global gen_num
    global lava_chance
    gen_num += 1
    lava_chance = (5/(1+math.exp(-.003*(gen_num-250)))) + \
        (5/(1+math.exp(-.0025*(gen_num-2000))))
    # Formats the lava chance into a percentage with 2 decimal places
    print("LAVA CHANCE:", str(round(lava_chance, 4)) + "%")
    board.lava_chance = lava_chance
    # Increases total frames by the percentage of the board that is lava
    # Agents will have to dodge lava more, meaning more frames are needed to finish
    max_frames = math.floor(175 + 4 * lava_chance)

    # Initialize pygame and neat arrays
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

    # Holds int for how many agents have reached the exit
    reached_exit = 0
    died = 0
    # Run the game
    for _ in range(0, max_frames):
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # For each agent, get the output from the network and move it
        agent_index = 0
        for _ in ge:
            agent = board.agent_list[agent_index]

            # Get fitness for staying alive
            #ge[agent_index].fitness += 1

            # Get adjacent cells
            adj = agent.get_adjacent_terrain()
            # Get the output from the network

            displacement_x = board.exit_x - agent.x
            displacement_y = board.exit_y - agent.y

            #0 - up, 1 - right, 2 - down, 3 - left
            output = nets[board.agent_list.index(agent)].activate((float(adj[0]),
                                                                   float(
                                                                       adj[1]),
                                                                   float(
                                                                       adj[2]),
                                                                   float(
                                                                       adj[3]),
                                                                   float(
                                                                       displacement_x),
                                                                   float(displacement_y)))

            #output = nets[board.agent_list.index(agent)].activate((float(displacement_x), float(displacement_y)))


            # Move the agent
            direction = output.index(max(output))
            if direction == 0:
                agent.move(0, 1)
            elif direction == 1:
                agent.move(1, 0)
            elif direction == 2:
                agent.move(0, -1)
            elif direction == 3:
                agent.move(0, 1)

            # Check if agent is dead
            if not agent.alive:
                # Loses flat 100 if agent dies
                ge[agent_index].fitness -= 100
                # Gets manhattan distance to exit
                distance = (abs(agent.x - board.exit_x)) + \
                    abs(agent.y - board.exit_y)
                # Use .75 as exponent to make fitness gain from distance weaker here because the agent died
                ge[agent_index].fitness += 750*(1 / distance**.75)
                # Removes the agent from the board as well as the network and genome
                died += 1
                board.alive_agents -= 1
                board.agent_list.remove(agent)
                nets.pop(agent_index)
                ge.pop(agent_index)
                agent_index -= 1
            elif agent.reached_exit():
                # Gives flat 1000 fitness for reaching the exit
                ge[agent_index].fitness += 1000
                # Gives them reward based on how many agents have already reached the exit
                reached_exit += 1
                ge[agent_index].fitness += 250*(1 / reached_exit**.5)
                # Removes the agent from the board as well as the network and genome
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

    # Add distance fitness to each genome
    agent_index = 0
    for _ in ge:
        #print("for agent in ge")
        agent = board.agent_list[agent_index]
        if agent.x <= constants.SAFE_ZONE_WIDTH:
            #print("didnt leave")
            ge[agent_index].fitness += -500
            #print("Agent fitness:", ge[agent_index].fitness)
            agent_index += 1
        else:
            distance = (abs(agent.x - board.exit_x)) + \
                abs(agent.y - board.exit_y)
            #print("Agent survived, adding distance to fitness", distance)
            ge[agent_index].fitness += 750*(1 / distance**.5)
            #print("Agent fitness:", ge[agent_index].fitness)
            agent_index += 1

    print("AGENTS DIED:", died)
    print("REACHED EXIT:", reached_exit)

    #board.run()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1176')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))
    winner = p.run(main, 100000)

    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner, output)


def test_ai(config):
    # Have to initialize a board

    with open('winner.pkl', 'rb') as input:
        winner = pickle.load(input)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.ini')
    run(config_path)
