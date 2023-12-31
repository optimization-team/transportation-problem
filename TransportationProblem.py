import numpy as np
import termtables as tt
from Exceptions import ImbalancedProblem, InfeasibleSolution
from input_parser import parse_input


class TransportationSolution:
    def __init__(self, solution, cost, basic=None):
        self.solution = solution
        self.cost = float(cost)
        self.basic = basic

    def __str__(self):
        table = []
        for i in range(self.solution.shape[0]):
            row = []
            for j in range(self.solution.shape[1]):
                if self.basic is not None and self.basic[i, j] == 1:
                    row.append(f"({self.solution[i, j]})")
                else:
                    row.append(self.solution[i, j])
            table.append(row)

        return f"Solution:\n{tt.to_string(table)}\nCost: {self.cost}\n"


class Transportation:
    def __init__(self, supply, demand, costs):
        self.costs = np.matrix(costs)
        self.supply = supply
        self.demand = demand
        self.n, self.m = self.costs.shape
        self.solution = np.zeros((self.n, self.m))
        self.basic = np.zeros((self.n, self.m))
        self.iteration = 0
        self.check_inputs()

    def check_inputs(self):
        if np.any(self.costs < 0) or np.any(np.array(self.supply) < 0) or np.any(np.array(self.demand) < 0):
            raise InfeasibleSolution()
        if sum(self.supply) != sum(self.demand):
            raise ImbalancedProblem()

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


class NorthwestCornerMethod(Transportation):
    def __init__(self, supply, demand, costs):
        super().__init__(supply, demand, costs)

    def solve(self) -> TransportationSolution:
        def northwest_corner_method_help(costs, supply, demand, solution, basic) -> TransportationSolution:
            row_index, column_index = 0, 0
            ans = 0.0
            while row_index <= (costs.shape[0] - 1) and column_index <= (costs.shape[1] - 1):
                if supply[row_index] <= demand[column_index]:
                    ans += supply[row_index] * costs.item((row_index, column_index))
                    demand[column_index] -= supply[row_index]
                    solution[row_index][column_index] = supply[row_index]
                    basic[row_index][column_index] = 1
                    row_index += 1
                else:
                    ans += demand[column_index] * costs.item((row_index, column_index))
                    supply[row_index] -= demand[column_index]
                    solution[row_index][column_index] = demand[column_index]
                    basic[row_index][column_index] = 1
                    column_index += 1
            return TransportationSolution(solution, ans, basic)

        return northwest_corner_method_help(
            self.costs.copy(),
            self.supply.copy(),
            self.demand.copy(),
            self.solution.copy(),
            self.basic.copy())


class VogelMethod(Transportation):
    def __init__(self, supply, demand, costs):
        super().__init__(supply, demand, costs)

    def solve(self) -> TransportationSolution:
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
                col_ids,
                basic) -> TransportationSolution:
            if costs.shape[0] == 1:
                for (col_id, elem) in zip(col_ids, demand):
                    solution[row_ids[0]][col_id] = elem
                    basic[row_ids[0]][col_id] = 1
                return TransportationSolution(
                    solution,
                    sum([a * b for (a, b) in zip(demand, costs[0])]) + total,
                    basic
                )
            if costs.shape[1] == 1:
                for (row_id, elem) in zip(row_ids, supply):
                    solution[row_id][col_ids[0]] = elem
                    basic[row_id][col_ids[0]] = 1
                return TransportationSolution(
                    solution,
                    sum([a * b for (a, b) in zip(supply, costs[:, 0])]) + total,
                    basic
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
                basic[row_ids[target_row_index], col_ids[target_col_index]] = 1
                return vogel_method_help(
                    new_consts,
                    new_supply,
                    new_demand,
                    target_elem * target_supply + total,
                    solution,
                    np.delete(row_ids, target_row_index),
                    col_ids,
                    basic)
            else:
                dif = target_supply - target_demand
                new_consts = np.delete(costs, target_col_index, axis=1)
                new_demand = np.delete(demand, target_col_index)
                new_supply = supply.copy()
                new_supply[target_row_index] = dif
                solution[row_ids[target_row_index], col_ids[target_col_index]] = target_demand
                basic[row_ids[target_row_index], col_ids[target_col_index]] = 1
                return vogel_method_help(
                    new_consts,
                    new_supply,
                    new_demand,
                    target_elem * target_demand + total,
                    solution,
                    row_ids,
                    np.delete(col_ids, target_col_index),
                    basic)

        return vogel_method_help(
            np.asarray(self.costs),
            self.supply.copy(),
            self.demand.copy(),
            0,
            self.solution.copy(),
            np.arange(self.costs.shape[0]),
            np.arange(self.costs.shape[1]),
            self.basic)


class RussellMethod(Transportation):
    def __init__(self, supply, demand, costs):
        super().__init__(supply, demand, costs)

    def solve(self):
        while True:
            # Find the highest cost value for each row and column for each source remaining under consideration
            u = np.zeros(self.n)
            v = np.zeros(self.m)
            for i in range(self.n):
                # check if row is still under consideration, if not, skip row
                if self.supply[i] == 0:
                    continue
                for j in range(self.m):
                    # check if column is still under consideration, if not, skip column
                    if self.demand[j] == 0:
                        continue
                    if self.solution[i, j] == 0 and self.costs[i, j] > u[i]:
                        u[i] = self.costs[i, j]
            for j in range(self.m):
                # check if column is still under consideration, if not, skip column
                if self.demand[j] == 0:
                    continue
                for i in range(self.n):
                    # check if row is still under consideration, if not, skip row
                    if self.supply[i] == 0:
                        continue
                    if self.solution[i, j] == 0 and self.costs[i, j] > v[j]:
                        v[j] = self.costs[i, j]

            delta = np.subtract(self.costs, np.add(u.reshape(self.n, 1), v.reshape(1, self.m)))

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
            self.basic[next_path[0], next_path[1]] = 1
            self.supply[next_path[0]] -= self.solution[next_path[0], next_path[1]]
            self.demand[next_path[1]] -= self.solution[next_path[0], next_path[1]]

            # check if all products are distributed (if all values in supply and demand are 0)
            if np.all(np.array(self.supply) == 0) and np.all(np.array(self.demand) == 0):
                break
        return TransportationSolution(self.solution, np.multiply(self.solution, self.costs).sum(), self.basic)
