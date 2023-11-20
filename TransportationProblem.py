import numpy as np
from Exceptions import ImbalancedProblem
import termtables as tt
import itertools
debug = False

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
        while True:
            # Find the highest cost value for each row and column for each source remaining under consideration
            u = np.zeros(self.n)
            v = np.zeros(self.m)
            for i in range(self.n):
                for j in range(self.m):
                    # check if row is still under consideration, if not, skip row
                    if self.supply[i] == 0:
                        continue
                    if self.solution[i, j] == 0 and self.costs[i, j] > u[i]:
                        u[i] = self.costs[i, j]
            for j in range(self.m):
                for i in range(self.n):
                    if self.demand[j] == 0:
                        continue
                    if self.solution[i, j] == 0 and self.costs[i, j] > v[j]:
                        v[j] = self.costs[i, j]

            delta = np.subtract(self.costs, np.add(u.reshape(self.n, 1), v.reshape(1, self.m)))

            if debug:
                print("Debug:")
                print(u)
                print(v)
                print(delta)

            # Select the variable having the largest (in absolute
            # terms) negative value of delta
            next_path = (0, 0)
            value = 0
            for i in range(self.n):
                for j in range(self.m):
                    if delta[i, j] < 0 and abs(delta[i, j]) > value:
                        value = abs(delta[i, j])
                        next_path = (i, j)

            # allocate goods or products on the cell
            self.solution[next_path[0], next_path[1]] = min(self.supply[next_path[0]], self.demand[next_path[1]])
            self.supply[next_path[0]] -= self.solution[next_path[0], next_path[1]]
            self.demand[next_path[1]] -= self.solution[next_path[0], next_path[1]]
            if debug:
                print("Solution:")
                print(self.solution)
                print(self.supply)
                print(self.demand)

            # check if all products are distributed (if all values in supply and demand are 0)
            if np.all(np.array(self.supply) == 0) and np.all(np.array(self.demand) == 0):
                break
        return TransportationSolution(self.solution, np.multiply(self.solution, self.costs).sum())


