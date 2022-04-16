# NeatDungeon

![Gif](https://imgur.com/poOU8Q4.gif)

## Brief overview
This creates a set amount of agents that can move up, down, left, and right.
During the first generation, their genetic structures are randomized, meaning they move mostly randomly.
Each generation lasts 150 frames, in other words, each generation allows each agent to make a total of 150 moves.
At the end of each generation, dependent on the distance away from the exit, a reward function is called and the result is added to the fitness of the specific agent.

Agents with similar gentic structures belong to the same "species".
Each species at the end of a generation has the fitnesses of their agents averaged.
Fitness is the total reward the agent has recieved depending on how close it got to the exit as well as how quick it got to the exit.
The species with higher fitnesses can reproduce more, and create more agents that are similar to them.
These species now have a chance to mutate either a new connection or node somewhere in between the input layer, the 1 hidden layer, or the end layer.
These new agents hopefully perform better than the previous ones, and continue to reproduce, creating new species with higher average fitnesses.


## Input/Output
The input layer has 6 values.
The first 4 inputs are cell types above it, below it, and on its left and right. This helps it hopefully differentiate from lava tiles (that will damage the agent), and safe tiles, such as the default "rock" cell.
The final two inputs are the displacement of the agents current x position and the exits x position, as well as the same, but for the y position.

The last two inputs seem to be the strongest for the agent and basically take over every time. I am currently trying to find a way to make the terrain type more important for the agent.

There are 4 outputs. Each is an number value for how much the agent wants to move in a direction. The max of these is taken and used to move the agent.


## Board
The board is filled with default "rock" cells that are safe for the agent to walk on. Lava is then placed randomly based on a percent, excluding 2 safe zones on each side.
Bridges can also be enabled to be placed to give the agents a safe path to walk across the lava in.

Note: As of right now the lava is static because I was testing something.


## Reward
Rewards are given based on Manhattan distance from the exit. The distance is the put into an exponential function to get reward. Reward is subtracted if the agent dies or stays in the safe zone and doesn't leave.
An extra bonus is given if the agent reaches the exit, which is reduced based on how many agents have already reached the exit.


## Other
This project is still somewhat messy but I am working on making this easy to set up and run.
There are comments throughout that explains most though.
