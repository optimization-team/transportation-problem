import numpy as np
from Exceptions import ImbalancedProblem
import termtables as tt


class TransportationSolution:
    def __init__(self, solution, cost):
        self.solution = solution
        self.cost = cost

    def __str__(self):
        # return f"Solution:\n {self.solution}\nCost: {self.cost}"
        # return a table without [[ and ]]
        table = []
        for i in range(self.solution.shape[0]):
            row = []
            for j in range(self.solution.shape[1]):
                row.append(self.solution[i, j])
            table.append(row)

        return f"Solution:\n{tt.to_string(table)}\nCost: {self.cost}"


class Transportation:

    def __init__(self, supply, demand, costs):
        self.costs = np.matrix(costs)
        self.supply = supply
        self.demand = demand
        self.n, self.m = self.costs.shape
        self.solution = np.zeros((self.n, self.m))
        self.iteration = 0
        self.check_inputs()

    def check_inputs(self):
        if sum(self.supply) != sum(self.demand):
            raise ImbalancedProblem()

    def print_initial_data(self):
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
        table = []
        header_row = [""] + [f"D_{i + 1}" for i in range(self.m)] + ["Supply"]
        header_row[0] = "Source, Dest"
        table.append(header_row)

        for i in range(self.n):
            row = [f"S_{i + 1}"] + [self.costs[i, j] for j in range(self.m)] + [self.supply[i]]
            table.append(row)

        demand_row = ["Demand"] + self.demand + [sum(self.supply)]
        table.append(demand_row)

        view = tt.to_string(
            table,
            style=tt.styles.rounded_thick
        )
        print(view)

    def north_west_corner_method(self):
        pass

    def vogel_method(self):
        pass

    def russell_method(self):

        u = np.zeros(self.n)
        v = np.zeros(self.m)
        delta = np.zeros((self.n, self.m))
        while True:
            # determine u_i
            for i in range(self.n):
                if self.supply[i] > 0:
                    u[i] = np.min(self.costs[i, :][self.costs[i, :] > 0])
            # determine v_j
            for j in range(self.m):
                if self.demand[j] > 0:
                    v[j] = np.min(self.costs[:, j][self.costs[:, j] > 0])
            # calculate delta
            for i in range(self.n):
                for j in range(self.m):
                    if self.costs[i, j] > 0:
                        delta[i, j] = self.costs[i, j] - u[i] - v[j]
            # select the variable having the largest (in absolute terms) negative value of delta
            min_delta = np.min(delta)

        return TransportationSolution(self.solution, np.sum(self.solution * self.costs.transpose()))


