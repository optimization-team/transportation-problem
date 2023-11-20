import numpy as np
from Exceptions import ImbalancedProblem
import termtables as tt
from input_parser import parse_input


class TransportationSolution:
    def __init__(self, solution, cost):
        self.solution = solution
        self.cost = cost


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

    def northwest_corner_method(self):
        row_index, column_index = 0, 0
        ans = 0
        while row_index <= (self.n - 1) and column_index <= (self.m - 1):
            if self.supply[row_index] <= self.demand[column_index]:
                ans += self.supply[row_index] * self.costs.item((row_index, column_index))
                self.demand[column_index] -= self.supply[row_index]
                row_index += 1
            else:
                ans += self.demand[column_index] * self.costs.item((row_index, column_index))
                self.supply[row_index] -= self.demand[column_index]
                column_index += 1
        return ans

    def vogel_method(self):
        pass

    def russell_method(self):
        pass


def main():
    supply, demand, costs = parse_input("inputs/input1.txt")

    transportation = Transportation(supply, demand, costs)
    transportation.print_initial_table()
    print("costs", transportation.costs)
    print("costs size", transportation.costs.shape[0], transportation.costs.shape[1])
    print("m", transportation.m)
    ans = transportation.northwest_corner_method()
    print("ans", ans)
    # print("ans", transportation.north_west_corner_method())


if __name__ == '__main__':
    main()
