# # Method checks the strength of the agent compared to the strength of the other agent in the cell and if the agent is stronger, pushes the other agent
    # def push_agent(self, other_agent):
    #     strength = self.get_strength()
    #     other_strength = other_agent.get_strength()
    #     # If the agent is stronger, pushes the other agent one cell in the direction it is moving
    #     if strength > other_strength:
    #         other_agent.move((self.x - self.previous_x) // constants.CELL_SIZE, (self.y - self.previous_y) // constants.CELL_SIZE)
    #         self.draw(self.board)
    #         other_agent.draw(self.board)
    #     else:
            
    #         # Remove the agent from the cell it is currently in
    #         self.board.cells[self.x // constants.CELL_SIZE][self.y // constants.CELL_SIZE].agent.remove(self)
    #         # Add the agent to the previous cell
    #         self.board.cells[self.previous_x // constants.CELL_SIZE][self.previous_y // constants.CELL_SIZE].agent.append(self)

    #         self.x = self.previous_x
    #         self.y = self.previous_y

    # # Randomly move agent around
    # while board.agent_count > 0:
    #     pygame.display.flip()
    #     #time.sleep(.05)
    #     board.randomly_move_agents()
    #     pygame.display.flip()
    #     #time.sleep(.1)

    # # Move up
    #             if output[0] > 0.5:
    #                 agent.move(0, 1)
    #             # Move down
    #             if output[1] > 0.5:
    #                 agent.move(0, -1)
    #             # Move left
    #             if output[2] > 0.5:
    #                 agent.move(-1, 0)
    #             # Move right
    #             if output[3] > 0.5:
    #                 agent.move(1, 0)
    #             # Move up-left
    #             if output[4] > 0.5:
    #                 agent.move(-1, 1)
    #             # Move up-right
    #             if output[5] > 0.5:
    #                 agent.move(1, 1)
    #             # Move down-left
    #             if output[6] > 0.5:
    #                 agent.move(-1, -1)
    #             # Move down-right
    #             if output[7] > 0.5:
    #                 agent.move(1, -1)




    while board.alive_agents > 0 and max_frames > 0:
    #     # Check for events
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit
    #             break
    #     # If the agent is dead, remove it from the board
    #     agent_index = 0
    #     for agent in board.agent_list:
    #         if not agent.alive:
    #                 ge[agent_index].fitness -= 50
    #                 nets.pop(board.agent_list.index(agent))
    #                 ge.pop(board.agent_list.index(agent))
    #                 board.agent_list.pop(board.agent_list.index(agent))
    #         agent_index += 1
                    
    #     # For each agent, get the output from the network and move the agent
    #     agent_index = 0
    #     for agent in ge:
    #         #print("GE LENGTHL", len(ge))
    #         agent = board.agent_list[agent_index]
    #         if agent.alive:
    #             # If the agent is in the same cell, it loses one fitness
    #             if agent.previous_x == agent.x and agent.previous_y == agent.y:
    #                 ge[agent_index].fitness -= 5

    #             ge[agent_index].fitness += 1

    #             adj = agent.get_adjacent_terrain()
    #             # The input is the
    #             output = nets[board.agent_list.index(agent)].activate((float(adj[0]), float(adj[1]), float(adj[2]), float(adj[3]), float(adj[4]), float(adj[5]), float(adj[6]),
    #                                                                    float(adj[7]), float(agent.x), float(agent.y), float(board.exit_x), float(board.exit_y)))
                
    #             direction = output.index(max(output))
                
    #             if direction == 0:
    #                 agent.move(-1,-1)
    #             elif direction == 1:
    #                 agent.move(0,-1)
    #             elif direction == 2:
    #                 agent.move(1,-1)
    #             elif direction == 3:
    #                 agent.move(-1,0)
    #             elif direction == 4:
    #                 agent.move(1,0)
    #             elif direction == 5:
    #                 agent.move(-1,1)
    #             elif direction == 6:
    #                 agent.move(0,1)
    #             elif direction == 7:
    #                 agent.move(1,1)

    #     pygame.display.flip()
    #     #time.sleep(.05)

    #     max_frames -= 1

    # agent_index = 0
    # for agent in ge:
    #     agent = board.agent_list[agent_index]
    #     if agent.alive:
    #         ge[agent_index].fitness += 5
    #         # Finds distance of agent to exit
    #     dist = abs(agent.x - board.exit_x) + abs(agent.y - board.exit_y)
    #     if dist == 0:
    #         ge[agent_index].fitness += 1000
    #     else:
    #         ge[agent_index].fitness += 25*(.25/dist)
            
    # # Save the winner
    # with open('winner.pkl', 'wb') as output:
    #     pickle.dump(ge[0], output, 1)