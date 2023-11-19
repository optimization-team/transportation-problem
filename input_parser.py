from numpy import matrix


def parse_input(filename: str) -> tuple:
    with open(filename) as file:
        supply = list(map(int, file.readline().split()))
        file.readline()
        demand = list(map(int, file.readline().split()))
        file.readline()
        costs = list()
        for line in file.readlines():
            costs.append(list(map(int, line.split())))
        return supply, demand, costs
