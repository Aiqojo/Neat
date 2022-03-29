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