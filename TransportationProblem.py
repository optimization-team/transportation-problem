import numpy as np
from Exceptions import InfeasibleSolution
import termtables as tt


class TransportationSolution:
    def __init__(self, solution, cost):
        self.solution = solution
        self.cost = cost


class Transportation:

    def __init__(self, supply, demand, costs):
        self.costs = np.matrix(costs)
        self.supply = supply
        self.demand = demand
        # self.n = len(costs)
        self.n, self.m = self.costs.shape
        self.solution = np.zeros((self.n, self.m))
        self.iteration = 0
        self.check_inputs()

    def check_inputs(self):
        if sum(self.supply) != sum(self.demand):
            raise InfeasibleSolution()

    def print_initial_data(self):
        # print data as a table with supply at the right and demand at the bottom

        print("Initial data:")
        print("Supply: ", end="")
        for i in range(self.n):
            print(f"{self.supply[i]} ", end="")
        print()
        print("Demand: ", end="")
        for i in range(self.m):
            print(f"{self.demand[i]} ", end="")
        print()
        print("Costs:")
        for i in range(self.n):
            for j in range(self.m):
                print(f"{self.costs[i, j]} ", end="")
            print()

    def print_initial_table(self):
        # print data as a table with supply at the right and demand at the bottom
        table = []
        header_row = [""] + [f"D_{i + 1}" for i in range(self.m)] + ["Supply"]
        # the first cell in the header row should have "source\destination" value
        header_row[0] = "Source, Dest"
        table.append(header_row)

        for i in range(self.n):
            row = [f"S_{i + 1}"] + [self.costs[i, j] for j in range(self.m)] + [self.supply[i]]
            table.append(row)

        # Add a row at the bottom with demand values and total supply
        demand_row = ["Demand"] + self.demand + [sum(self.supply)]
        table.append(demand_row)

        # visualize the table using tabulate
        view = tt.to_string(
            table,
            style=tt.styles.rounded_thick
        )
        print(view)

    def minimal_element_method(self):
        pass

    def north_west_corner_method(self):
        pass

    def vogel_method(self):
        pass
