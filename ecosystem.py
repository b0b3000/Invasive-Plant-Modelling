from Cell2D import Cell2D, draw_array
import numpy as np
import matplotlib.pyplot as plt
from numpy import random

from plant import Plant


class Ecosystem(Cell2D):
    """Represents a given ecoystem."""

    def __init__(self, n: int, params: dict):
        """Initializes the attributes.
        n: number of rows and columns
        params: dictionary of parameters
        """

        self.n = n
        self.params = params
        self.agents = list(params.get("plants"))
        self.occupied = [agent.loc for agent in self.agents]
        self.competition_constant = params.get("competition_constant")
        self.array = np.zeros((n,n))

    def make_agents(self, agents: dict[Plant, str]):
        """
        Populate the ecoystem with flora.
        This function takes given, specified
        plants populates the ecosystem with them. 
        """
        for current_agent in agents:
            self.add_plant(current_agent)

    def add_plant(self, agent: Plant):
        """Add a given plant to the ecosystem"""

        self.agents.append(agent)
        self.occupied.append(agent.loc)
    
    def remove_plant(self, agent: Plant):
        """ Remove a plant from the ecosystem"""
        self.agents.remove(agent)
        self.occupied.remove(agent.loc)

    def get_neighbours(self, agent: Plant):
        loc_row = agent.loc[0]
        loc_column = agent.loc[1]

        row_start = max(0, loc_row-1)
        row_end = min(self.array.shape[0], loc_row+2)
        
        col_start = max(0, loc_column-1)
        col_end = min(self.array.shape[1], loc_column+2)

        neighbours = []
        for row in range(row_start, row_end):
            for col in range(col_start, col_end):
                # Exclude the current plant itself
                if not (row == loc_row and col == loc_column):
                    neighbours.append((row,col))
         
        return neighbours

    def get_empty_neighbours(self, agent: Plant):
        # Define the range for rows and columns, ensuring the indices don't go out of bounds

        neighbours = self.get_neighbours(agent)
        empty_neighbours = []

        for neighbour in neighbours:
            if not (neighbour in self.occupied):
                empty_neighbours.append(neighbour)

        return empty_neighbours
    
    def get_occupied_neighbours_agents(self, agent: Plant):
        neighbours = self.get_neighbours(agent)
        occupied_neighbours = []

        for neighbour in neighbours:
            if (neighbour in self.occupied):
                for each_agent in self.agents:
                    if each_agent.loc == neighbour:
                        occupied_neighbours.append(each_agent)
        return occupied_neighbours
    
    def check_competition(self, agent: Plant):
        occupied_neighbours = self.get_occupied_neighbours_agents(agent)
        if not occupied_neighbours is None:
            for neighbour in occupied_neighbours:
                random_zero_to_one = random.random()
                if random_zero_to_one < self.competition_constant:
                    if agent.size + agent.resilience > neighbour.size + neighbour.resilience:
                        self.remove_plant(neighbour)
                    else:
                        self.remove_plant(agent)
                        return
        

    def step(self):
        """Executes one time step."""

        # loop through the agents in random order
        random_order = np.random.permutation(self.agents)
        for agent in random_order:
            if agent in self.agents: #might have been removed midway
                agent.step()

                # If the agent plant is too old, remove from the ecosystem
                if agent.is_old():
                    self.remove_plant(agent)

                else:
                    # Generate plant(s) next to the current one
                    offspring = agent.reproduce(self)
                    if len(offspring) != 0:
                        for new_plant in offspring:
                            self.add_plant(new_plant)

                    self.check_competition(agent)

        return len(self.agents)

    def draw(self):
        """Draws the ecosystem as a cellular automata grid."""
        # Clear the previous figure
        plt.clf()

        # Update the array based on the positions of the agents
        for agent in self.agents:
            self.array[agent.loc] = 1  # You can use different values for different states or types

        # Draw the ecosystem grid
        plt.imshow(self.array, cmap='YlOrRd', vmin=0, vmax=1, origin='lower')
        plt.gca().axes.get_xaxis().set_visible(False)  # Hide x-axis
        plt.gca().axes.get_yaxis().set_visible(False)   
        plt.title('Ecosystem Cellular Automata Visualization')
        plt.show()

        # Reset the array to zero for the next step
        self.array.fill(0)

    def get_coords(self):
        """Gets the coordinates of the agents.

        Transforms from (row, col) to (x, y).

        returns: tuple of sequences, (xs, ys)
        """
        rows, cols = np.transpose([agent.loc for agent in self.agents])
        xs = cols + 0.5
        ys = rows + 0.5
        return xs, ys