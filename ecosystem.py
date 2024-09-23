from scipy.signal import correlate2d
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
        self.agents = list[Plant]
        self.occupied = list[tuple]

        self.array = np.array(n,n)

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
        self.agents.pop(agent)
        self.occupied.pop(agent.loc)


    def get_empty_cells(self, agent: Plant):
        # Define the range for rows and columns, ensuring the indices don't go out of bounds
        loc_row = agent.loc[0]
        loc_column = agent.loc[1]

        row_start = max(0, loc_row-1)
        row_end = min(self.array.shape[0], loc_row+2)
        
        col_start = max(0, loc_column-1)
        col_end = min(self.array.shape[1], loc_column+2)
        
        # Collect the neighboring coordinates
        neighbors = []
        for row in range(row_start, row_end):
            for col in range(col_start, col_end):
                # Exclude the current plant itself
                if row == loc_row and col == loc_column:
                    continue
                for loc in self.occupied:
                    if loc == (row,loc):
                    # We have a neighbour!
                        neighbors.append(loc)
        return neighbors

    def step(self):
        """Executes one time step."""

        # loop through the agents in random order
        random_order = np.random.permutation(self.agents.items())
        for agent in random_order:

            # execute one step that updates the agent's new location and sugar level
            agent.step(self)

            # If the agent plant is too old, remove from the ecosystem
            if agent.is_old():
                self.remove_plant(agent)

            if agent.can_reproduce():
                # Calculate where it can reproduce
                empty_cells = self.get_empty_cells(agent)
                # Generate a plant next to the current one
                offspring = agent.reproduce(self)
                """ TODO: determine whether it should grow more than once at a time"""
                for new_plant in offspring:
                    self.add_plant(new_plant)

        return len(self.agents)

    def draw(self):
        """Draws the cells."""
        draw_array(self.array, cmap='YlOrRd', vmax=9, origin='lower')

        # draw the agents
        xs, ys = self.get_coords()
        self.points = plt.plot(xs, ys, '.', color='red')[0]

    def get_coords(self):
        """Gets the coordinates of the agents.

        Transforms from (row, col) to (x, y).

        returns: tuple of sequences, (xs, ys)
        """
        agents = self.agents
        rows, cols = np.transpose([agent.loc for agent in agents])
        xs = cols + 0.5
        ys = rows + 0.5
        return xs, ys