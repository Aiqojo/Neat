import Board, pygame, time, constants, Agent, random, os, neat


def main(genomes, config):
    pygame.init()

    nets = []
    ge = []

    # Create the board and agents
    board = Board.Board()
    for i in range(20):
        agent = Agent.Agent(board, i)
        board.add_agent(agent)

    for g in genomes:
        net = neat.nn.FeedForwardNetwork(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    generations = 100

    for i in range(generations):
        while board.agent_count > 0:
            for x, agent in enumerate(board.agent_list):
                


    

    board.run()

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
