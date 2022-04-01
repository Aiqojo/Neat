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