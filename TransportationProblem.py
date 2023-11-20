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

    def northwest_corner_method(self) -> TransportationSolution:
        def northwest_corner_method_help(costs, supply, demand, solution) -> TransportationSolution:
            row_index, column_index = 0, 0
            ans = 0
            while row_index <= (costs.shape[0] - 1) and column_index <= (costs.shape[1] - 1):
                if supply[row_index] <= demand[column_index]:
                    ans += supply[row_index] * costs.item((row_index, column_index))
                    demand[column_index] -= supply[row_index]
                    solution[row_index][column_index] = supply[row_index]
                    row_index += 1
                else:
                    ans += demand[column_index] * costs.item((row_index, column_index))
                    supply[row_index] -= demand[column_index]
                    solution[row_index][column_index] = demand[column_index]
                    column_index += 1
            return TransportationSolution(solution, ans)

        return northwest_corner_method_help(
            self.costs.copy(),
            self.supply.copy(),
            self.demand.copy(),
            self.solution.copy())

    def vogel_method(self) -> TransportationSolution:
        def find_difference(costs):
            row_difference = []
            column_difference = []
            for i in range(costs.shape[0]):
                arr = sorted(costs[i])
                row_difference.append(arr[1] - arr[0])
            column_index = 0
            while column_index < len(costs[0]):
                arr = []
                for i in range(costs.shape[0]):
                    arr.append(costs[i][column_index])
                arr = sorted(arr)
                column_index += 1
                column_difference.append(arr[1] - arr[0])
            return row_difference, column_difference

        def vogel_method_help(
                costs: np.ndarray,
                supply,
                demand,
                total,
                solution,
                row_ids,
                col_ids) -> TransportationSolution:
            if costs.shape[0] == 1:
                for (col_id, elem) in zip(col_ids, demand):
                    solution[row_ids[0]][col_id] = elem
                return TransportationSolution(
                    solution,
                    sum([a * b for (a, b) in zip(demand, costs[0])]) + total
                )
            if costs.shape[1] == 1:
                for(row_id, elem) in zip(row_ids, supply):
                    solution[row_id][col_ids[0]] = elem
                return TransportationSolution(
                    solution,
                    sum([a * b for (a, b) in zip(supply, costs[:, 0])]) + total
                )

            row_differences, column_differences = find_difference(costs)
            max_row_dif_index, max_row_dif = max(zip(range(costs.shape[0]), row_differences), key=lambda x: x[1])
            max_col_dif_index, max_col_dif = max(zip(range(costs.shape[1]), column_differences), key=lambda x: x[1])

            if max_row_dif >= max_col_dif:
                row = costs[max_row_dif_index]
                target_col_index, min_col_elem = min(zip(range(costs.shape[1]), row), key=lambda x: x[1])
                target_row_index = max_row_dif_index
            else:
                col = costs[:, max_col_dif_index]
                target_row_index, min_row_elem = min(zip(range(costs.shape[0]), col), key=lambda x: x[1])
                target_col_index = max_col_dif_index

            target_elem = costs[target_row_index][target_col_index]
            target_supply = supply[target_row_index]
            target_demand = demand[target_col_index]

            if target_demand > target_supply:
                dif = target_demand - target_supply
                new_consts = np.delete(costs, target_row_index, axis=0)
                new_supply = np.delete(supply, target_row_index)
                new_demand = demand.copy()
                new_demand[target_col_index] = dif
                solution[row_ids[target_row_index], col_ids[target_col_index]] = target_supply
                return vogel_method_help(
                    new_consts,
                    new_supply,
                    new_demand,
                    target_elem * target_supply + total,
                    solution,
                    np.delete(row_ids, target_row_index),
                    col_ids)
            else:
                dif = target_supply - target_demand
                new_consts = np.delete(costs, target_col_index, axis=1)
                new_demand = np.delete(demand, target_col_index)
                new_supply = supply.copy()
                new_supply[target_row_index] = dif
                solution[row_ids[target_row_index], col_ids[target_col_index]] = target_demand
                return vogel_method_help(
                    new_consts,
                    new_supply,
                    new_demand,
                    target_elem * target_demand + total,
                    solution,
                    row_ids,
                    np.delete(col_ids, target_col_index))

        return vogel_method_help(
            np.asarray(self.costs),
            self.supply.copy(),
            self.demand.copy(),
            0,
            self.solution.copy(),
            np.arange(self.costs.shape[0]),
            np.arange(self.costs.shape[1]))

    def russell_method(self):
        pass


def main():
    # supply, demand, costs = parse_input("inputs/input3.txt")
    #
    # transportation = Transportation(supply, demand, costs)
    # transportation.print_initial_table()
    # print("costs", transportation.costs)
    # print("costs size", transportation.costs.shape[0], transportation.costs.shape[1])
    # print("m", transportation.m)
    #
    # solution = transportation.northwest_corner_method()
    # print("ans", solution.cost)
    # print("solution\n", solution.solution)

    supply, demand, costs = parse_input("inputs/input2.txt")

    transportation = Transportation(supply, demand, costs)
    transportation.print_initial_table()
    print("costs", transportation.costs)
    print("costs size", transportation.costs.shape[0], transportation.costs.shape[1])
    print("m", transportation.m)
    solution = transportation.vogel_method()
    print("ans", solution.cost)
    print("solution\n", solution.solution)


if __name__ == '__main__':
    main()
