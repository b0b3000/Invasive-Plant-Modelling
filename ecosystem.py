from scipy.signal import correlate2d
from Cell2D import Cell2D, draw_array
import numpy as np
import matplotlib.pyplot as plt

from plant import Plant


class Ecosystem(Cell2D):
    """Represents a given ecoystem."""

    def __init__(self, n: int, **params: dict):
        """Initializes the attributes.
        n: number of rows and columns
        params: dictionary of parameters
        """

        self.n = n
        self.params = params
        self.agents = {}

        self.array = np.array(n,n)

    def make_agents(self, agents: dict[Plant, str]):
        """Populate the ecoystem with flora."""
        for current_agent in agents:
            self.agents.update({current_agent.loc: current_agent})

    def add_agent(self, agent: Plant):
        """Add a given agent to the ecosystem"""
        self.agents.update({agent.loc: agent})
        return 0

    def reproduce(self):
        """Go throug all plants, and check if any can reproduce"""
        return 0

    def step(self):
        """Executes one time step."""
        replace = self.params.get('replace', False)

        # loop through the agents in random order
        random_order = np.random.permutation(self.agents)
        for agent in random_order:

            # mark the current cell unoccupied
            self.occupied.remove(agent.loc)

            # execute one step that updates the agent's new location and sugar level
            agent.step(self)

            # if the agent is dead, remove from the list
            if agent.is_starving() or agent.is_old():
                self.agents.remove(agent)
                if replace:
                    self.add_agent()
            else:
                # otherwise mark its cell occupied
                self.occupied.add(agent.loc)

        # update the time series
        self.agent_count_seq.append(len(self.agents))

        # grow back some sugar
        self.grow()
        return len(self.agents)

    def add_agent(self):
        """Generates a new random agent.

        returns: new Agent
        """
        new_agent = Plant(self.random_loc(), self.params)
        self.agents.append(new_agent)
        self.occupied.add(new_agent.loc)
        return new_agent

    def random_loc(self):
        """Choose a random unoccupied cell.

        returns: tuple coordinates
        """
        while True:
            loc = tuple(np.random.randint(self.n, size=2))
            if loc not in self.occupied:
                return loc

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